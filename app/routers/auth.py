from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ..models.auth import User, TokenBlacklist
from ..services.email import send_confirmation_email
from ..core.security import create_access_token, create_refresh_token, decode_token
from ..db import get_db

router = APIRouter(prefix="/auth")


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    token = str(uuid4())
    user = User(
        email=data.email,
        hashed_password=data.password,
        first_name=data.name,
        email_confirmation_token=token,
        is_active=False,
    )
    db.add(user)
    db.commit()
    send_confirmation_email(data.email, token)
    return {"detail": "Confirmation email sent"}


@router.post("/token", response_model=TokenResponse)
def login(data: TokenRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or user.hashed_password != data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token(str(user.id))
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    jti = payload.get("jti")
    if db.query(TokenBlacklist).filter_by(jti=jti).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")
    user_id = payload.get("sub")
    access = create_access_token({"sub": user_id})
    refresh_token = create_refresh_token(user_id)
    return TokenResponse(access_token=access, refresh_token=refresh_token)


@router.post("/logout")
def logout(data: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token)
    jti = payload.get("jti")
    db.add(TokenBlacklist(jti=jti, expires_at=datetime.fromtimestamp(payload["exp"])))
    db.commit()
    return {"detail": "Logged out"}


@router.get("/confirm")
def confirm_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email_confirmation_token=token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    user.is_active = True
    user.email_confirmation_token = None
    db.commit()
    return {"detail": "Email confirmed"}
