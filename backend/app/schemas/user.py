from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.models.user import UserRole, UserStatus


# ── Base Model ──────────────────────────────────────────────────────
class UserBase(BaseModel):
    name: str
    email: str
    role: UserRole


# ── Create ──────────────────────────────────────────────────────────
class UserCreate(UserBase):
    password: str


# ── Update ──────────────────────────────────────────────────────────
class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None


# ── Response ────────────────────────────────────────────────────────
class UserResponse(UserBase):
    id: int
    status: str
    last_login: Optional[datetime]
    mfa_enabled: bool

    class Config:
        from_attributes = True
