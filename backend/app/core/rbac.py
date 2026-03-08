"""
core/rbac.py — Role-Based Access Control

Every protected endpoint uses one of the dependency functions below.
Usage in a route:
    @router.get("/dam/status")
    async def get_status(current_user: User = Depends(require_water_access)):
        ...
"""
from fastapi import Depends, HTTPException, status
from app.core.auth import get_current_active_user
from app.models.user import User, UserRole


# ------------------------------------------------------------------
# Permission groups
# ------------------------------------------------------------------

WATER_MANAGEMENT_ROLES = {
    UserRole.DIRECTOR,
    UserRole.OPERATOR,
    UserRole.AGRICULTURAL_OFFICER,
}

RELEASE_ORDER_SUBMIT_ROLES = {
    UserRole.DIRECTOR,
    UserRole.OPERATOR,
}

APPROVE_ORDER_ROLES = {
    UserRole.DIRECTOR,
}

THRESHOLD_CHANGE_ROLES = {
    UserRole.DIRECTOR,
}

AUDIT_LOG_VIEW_ROLES = {
    UserRole.DIRECTOR,
    UserRole.ADMIN,
}

ADMIN_ROLES = {
    UserRole.ADMIN,
}


# ------------------------------------------------------------------
# Dependency factories
# ------------------------------------------------------------------

def _require_roles(allowed_roles: set):
    async def checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not permitted to perform this action.",
            )
        return current_user
    return checker


def require_water_access(current_user: User = Depends(get_current_active_user)):
    """Director, Operator, Agricultural Officer — anyone with water visibility."""
    if current_user.role not in WATER_MANAGEMENT_ROLES:
        raise HTTPException(status_code=403, detail="Water data access denied.")
    return current_user


require_can_submit_order = _require_roles(RELEASE_ORDER_SUBMIT_ROLES)
require_can_approve_order = _require_roles(APPROVE_ORDER_ROLES)
require_director = _require_roles({UserRole.DIRECTOR})
require_admin = _require_roles(ADMIN_ROLES)
require_audit_log_access = _require_roles(AUDIT_LOG_VIEW_ROLES)
