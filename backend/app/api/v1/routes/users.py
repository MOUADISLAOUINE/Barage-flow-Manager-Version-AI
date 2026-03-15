"""
User CRUD endpoints.
Restricted to Admin users only.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.core import security
from app.core.rbac import RequireRole
from app.models.user import User, UserRole, UserStatus
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.api.v1.routes.auth import log_audit_event

# All routes in this router require the 'Admin' role
router = APIRouter(
    tags=["Users"],
    dependencies=[Depends(RequireRole([UserRole.ADMIN.value]))]
)


@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all users. Admin only."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID. Admin only."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    request: Request,
    user_in: UserCreate, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(RequireRole([UserRole.ADMIN.value]))
):
    """Create a new user. Admin only."""
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user record
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        role=user_in.role.value,
        password_hash=security.get_password_hash(user_in.password),
        status=UserStatus.ACTIVE.value
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Log action
    ip_address = request.client.host if request.client else None
    log_audit_event(
        db=db, 
        action="CREATE_USER", 
        user=current_admin, 
        ip=ip_address, 
        target_entity="User", 
        target_id=new_user.id
    )

    return new_user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    request: Request,
    user_id: int, 
    user_in: UserUpdate, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(RequireRole([UserRole.ADMIN.value]))
):
    """Update a user's details (role, status, name). Admin only."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admins from demoting/suspending themselves to avoid lockout
    if user.id == current_admin.id:
        if user_in.role and user_in.role != UserRole.ADMIN:
            raise HTTPException(status_code=400, detail="Cannot downgrade your own Admin role")
        if user_in.status and user_in.status == UserStatus.SUSPENDED:
            raise HTTPException(status_code=400, detail="Cannot suspend your own account")

    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if isinstance(value, (UserRole, UserStatus)):
            value = value.value
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    # Log action
    ip_address = request.client.host if request.client else None
    log_audit_event(
        db=db, 
        action="UPDATE_USER", 
        user=current_admin, 
        ip=ip_address, 
        target_entity="User", 
        target_id=user.id
    )

    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    request: Request,
    user_id: int, 
    db: Session = Depends(get_db),
    current_admin: User = Depends(RequireRole([UserRole.ADMIN.value]))
):
    """Suspend a user (soft delete). Never hard deletes. Admin only."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot suspend your own account")

    user.status = UserStatus.SUSPENDED.value
    db.commit()

    # Log action
    ip_address = request.client.host if request.client else None
    log_audit_event(
        db=db, 
        action="SUSPEND_USER", 
        user=current_admin, 
        ip=ip_address, 
        target_entity="User", 
        target_id=user.id
    )

    return {"detail": f"User {user.email} successfully suspended"}
