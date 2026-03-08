"""
api/v1/routes/dam.py — Live dam status endpoint
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models.dam import Dam
from app.core.rbac import require_water_access
from app.models.user import User

router = APIRouter()


class DamStatusResponse(BaseModel):
    id: int
    name: str
    current_level_m3: float
    current_level_pct: float
    current_zone: str
    safety_lock_active: bool
    safety_reserve_pct: float
    max_capacity_m3: float
    last_reading_at: datetime

    class Config:
        from_attributes = True


@router.get("/status", response_model=DamStatusResponse)
async def get_dam_status(
    dam_id: int = 1,
    current_user: User = Depends(require_water_access),
    db: Session = Depends(get_db),
):
    dam = db.query(Dam).filter(Dam.id == dam_id).first()
    if not dam:
        raise HTTPException(status_code=404, detail="Dam not found.")
    return dam


@router.patch("/thresholds")
async def update_safety_threshold(
    dam_id: int,
    safety_reserve_pct: float,
    current_user: User = Depends(require_water_access),
    db: Session = Depends(get_db),
):
    """Director only — update the configurable safety reserve threshold."""
    from app.core.rbac import require_director
    from app.services.audit_service import write_audit_log
    from app.models.user import UserRole

    if current_user.role != UserRole.DIRECTOR:
        raise HTTPException(status_code=403, detail="Only the Director can change safety thresholds.")

    dam = db.query(Dam).filter(Dam.id == dam_id).first()
    if not dam:
        raise HTTPException(status_code=404, detail="Dam not found.")

    before = {"safety_reserve_pct": dam.safety_reserve_pct}
    dam.safety_reserve_pct = safety_reserve_pct
    db.commit()

    write_audit_log(db, current_user, "THRESHOLD_CHANGED", "Dam", dam.id,
                    data_before=before, data_after={"safety_reserve_pct": safety_reserve_pct})
    return {"message": "Threshold updated.", "new_safety_reserve_pct": safety_reserve_pct}
