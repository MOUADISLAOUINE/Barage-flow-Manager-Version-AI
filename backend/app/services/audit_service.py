"""
services/audit_service.py

Rule 4 — The Immutable Audit Trail.
Every significant action goes through write_audit_log().
This function ONLY appends — it never updates or deletes.
"""
from datetime import datetime
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.user import Utilisateur as User


def write_audit_log(
    db: Session,
    user: User,
    action: str,
    resource_type: str,
    resource_id: Optional[int] = None,
    data_before: Optional[Any] = None,
    data_after: Optional[Any] = None,
    extra_notes: Optional[str] = None,
    ip_address: Optional[str] = None,
    session_id: Optional[str] = None,
) -> AuditLog:
    """
    Append a permanent record to the audit log.
    Called by every service function that modifies water data.

    Common action strings:
        USER_LOGIN, USER_LOGOUT
        RELEASE_ORDER_SUBMITTED, RELEASE_ORDER_APPROVED,
        RELEASE_ORDER_REJECTED, RELEASE_ORDER_BLOCKED
        SAFETY_LOCK_OVERRIDE
        THRESHOLD_CHANGED
        CONTRACT_MODIFIED
        AI_ANOMALY_DETECTED
        AI_ANOMALY_RESOLVED
    """
    log_entry = AuditLog(
        user_id=user.id,
        user_name=user.full_name,
        user_role=user.role.value,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        data_before=data_before,
        data_after=data_after,
        extra_notes=extra_notes,
        timestamp=datetime.utcnow(),
        ip_address=ip_address,
        session_id=session_id,
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
