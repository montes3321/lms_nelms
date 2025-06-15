from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class PermissionRead(BaseModel):
    id: int
    code: str
    description: Optional[str]

    class Config:
        orm_mode = True

class RoleRead(BaseModel):
    id: int
    slug: str
    title: str
    permissions: List[PermissionRead] = []

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    phone: Optional[str]
    password: str
    first_name: Optional[str]
    last_name: Optional[str]

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    phone: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    roles: List[RoleRead] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
