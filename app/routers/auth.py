from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ..models.auth import User, TokenBlacklist
from ..core.security import create_access_token, create_refresh_token, decode_token
from ..db import get_db

router = APIRouter(prefix="/auth")


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


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
