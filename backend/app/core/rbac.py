"""
Role-Based Access Control (RBAC) Middleware.
Provides dependency injection to enforce user roles on specific endpoints.
"""

from typing import List
from fastapi import Depends, HTTPException, status

from app.core.auth import get_current_active_user
from app.models.user import User


class RequireRole:
    """
    Dependency class to enforce role-based access.
    Usage: Depends(RequireRole(["Admin", "Director"]))
    """
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Requires one of: {', '.join(self.allowed_roles)}"
            )
        return current_user

# Usage shortcut examples:
# admin_only = Depends(RequireRole([UserRole.ADMIN.value]))
