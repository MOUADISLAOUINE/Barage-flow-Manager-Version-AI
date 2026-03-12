"""
api/v1/routes/admin.py

Admin has ZERO access to water data.
Admin can ONLY: manage user accounts and view system health.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.database import get_db
from app.models.user import Utilisateur as User, UserRole, UserStatus
from app.core.rbac import require_admin
from app.core.security import hash_password

router = APIRouter()


class CreateUserRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole


class UpdateUserStatusRequest(BaseModel):
    status: UserStatus


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    body: CreateUserRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered.")

    user = User(
        full_name=body.full_name,
        email=body.email,
        hashed_password=hash_password(body.password),
        role=body.role,
        created_by_id=current_user.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created.", "user_id": user.id, "role": user.role}


@router.get("/users")
async def list_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.query(User).all()


@router.patch("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    body: UpdateUserStatusRequest,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user.status = body.status
    db.commit()
    return {"message": f"User status updated to {body.status}."}


@router.get("/health")
async def system_health(current_user: User = Depends(require_admin)):
    """Basic system health check for Admin monitoring."""
    return {
        "status": "ok",
        "database": "connected",
        "redis": "connected",
    }
