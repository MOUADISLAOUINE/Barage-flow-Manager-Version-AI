"""
services/dam_service.py

Core dam business logic:
  - Zone calculation
  - Safety lock enforcement
  - Water level updates
"""
from datetime import datetime
from sqlalchemy.orm import Session

from app.config import settings
from app.models.dam import Barrage as Dam, WaterZone
from app.models.audit_log import AuditLog
from app.models.release_order import OrderStatus, ReleaseOrder
from app.models.user import Utilisateur as User
from app.services.audit_service import write_audit_log


def calculate_zone(level_pct: float, dam: Dam) -> WaterZone:
    """
    Determine the WaterZone from a percentage level.
    Thresholds are read from the Dam record — never hard-coded.
    """
    safety_pct = dam.safety_reserve_pct  # e.g. 25%
    warning_pct = safety_pct + 15        # e.g. 40%
    alert_pct = warning_pct + 20         # e.g. 60%

    if level_pct < safety_pct:
        return WaterZone.CRITICAL
    elif level_pct < warning_pct:
        return WaterZone.WARNING
    elif level_pct < alert_pct:
        return WaterZone.ALERT
    else:
        return WaterZone.NORMAL


def update_dam_level(db: Session, dam: Dam, new_level_m3: float) -> Dam:
    """
    Update dam water level, recalculate zone, engage/disengage safety lock.
    Called after each sensor reading is ingested.
    """
    old_pct = dam.current_level_pct
    new_pct = (new_level_m3 / dam.max_capacity_m3) * 100

    dam.current_level_m3 = new_level_m3
    dam.current_level_pct = round(new_pct, 2)
    dam.last_reading_at = datetime.utcnow()

    new_zone = calculate_zone(new_pct, dam)
    old_zone = dam.current_zone

    dam.current_zone = new_zone
    dam.safety_lock_active = (new_zone == WaterZone.CRITICAL)

    # If safety lock just engaged, block all pending orders
    if dam.safety_lock_active:
        _block_pending_orders(db, dam)

    db.commit()
    db.refresh(dam)
    return dam


def _block_pending_orders(db: Session, dam: Dam):
    """Block all PENDING release orders when safety lock activates."""
    pending = (
        db.query(ReleaseOrder)
        .filter(
            ReleaseOrder.dam_id == dam.id,
            ReleaseOrder.status == OrderStatus.PENDING,
        )
        .all()
    )
    for order in pending:
        order.status = OrderStatus.BLOCKED
        order.notes = (order.notes or "") + " | Auto-blocked: safety lock engaged."
    db.commit()


def can_submit_release_order(dam: Dam) -> tuple[bool, str]:
    """
    Returns (allowed: bool, reason: str).
    The operator UI should call this before showing the submit button.
    """
    if dam.safety_lock_active or dam.current_zone == WaterZone.CRITICAL:
        return False, "Safety lock active — reservoir is in CRITICAL zone. Director MFA override required."
    if dam.current_zone == WaterZone.WARNING:
        return False, "Reservoir is in WARNING zone — operator releases blocked. Director must approve manually."
    return True, "OK"
