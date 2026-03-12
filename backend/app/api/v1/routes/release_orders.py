"""
api/v1/routes/release_orders.py

Endpoints for the full release order lifecycle:
  Submit → Director Review → Approve/Reject
  Safety Lock Override (Director + MFA only)
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.database import get_db
from app.models.release_order import ReleaseOrder, OrderStatus
from app.models.user import Utilisateur as User, UserRole
from app.core.rbac import require_can_submit_order, require_can_approve_order, require_director
from app.core.security import verify_mfa_token
from app.services.dam_service import can_submit_release_order
from app.services.audit_service import write_audit_log
from app.models.dam import Barrage as Dam

router = APIRouter()


class SubmitOrderRequest(BaseModel):
    dam_id: int
    cooperative_id: Optional[int] = None
    volume_m3: float
    scheduled_release_at: Optional[datetime] = None
    notes: Optional[str] = None


class ApproveOrderRequest(BaseModel):
    notes: Optional[str] = None


class OverrideRequest(BaseModel):
    mfa_code: str
    justification: str  # Mandatory — Rule 1


class OrderResponse(BaseModel):
    id: int
    status: str
    volume_m3: float
    requested_at: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def submit_release_order(
    request: Request,
    body: SubmitOrderRequest,
    current_user: User = Depends(require_can_submit_order),
    db: Session = Depends(get_db),
):
    dam = db.query(Dam).filter(Dam.id == body.dam_id).first()
    if not dam:
        raise HTTPException(status_code=404, detail="Dam not found.")

    allowed, reason = can_submit_release_order(dam)
    if not allowed:
        raise HTTPException(status_code=403, detail=reason)

    order = ReleaseOrder(
        requested_by_id=current_user.id,
        dam_id=body.dam_id,
        cooperative_id=body.cooperative_id,
        volume_m3=body.volume_m3,
        status=OrderStatus.PENDING,
        scheduled_release_at=body.scheduled_release_at,
        notes=body.notes,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    write_audit_log(
        db, current_user, "RELEASE_ORDER_SUBMITTED", "ReleaseOrder", order.id,
        data_after={"volume_m3": order.volume_m3, "status": order.status},
        ip_address=request.client.host,
    )
    return order


@router.patch("/{order_id}/approve")
async def approve_order(
    order_id: int,
    request: Request,
    body: ApproveOrderRequest,
    current_user: User = Depends(require_can_approve_order),
    db: Session = Depends(get_db),
):
    order = db.query(ReleaseOrder).filter(ReleaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"Cannot approve order with status '{order.status}'.")

    before = {"status": order.status}
    order.status = OrderStatus.APPROVED
    order.approved_by_id = current_user.id
    order.decided_at = datetime.utcnow()
    order.notes = body.notes
    db.commit()

    write_audit_log(
        db, current_user, "RELEASE_ORDER_APPROVED", "ReleaseOrder", order.id,
        data_before=before, data_after={"status": order.status},
        ip_address=request.client.host,
    )
    return {"message": "Order approved.", "order_id": order_id}


@router.patch("/{order_id}/reject")
async def reject_order(
    order_id: int,
    request: Request,
    body: ApproveOrderRequest,
    current_user: User = Depends(require_can_approve_order),
    db: Session = Depends(get_db),
):
    order = db.query(ReleaseOrder).filter(ReleaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    before = {"status": order.status}
    order.status = OrderStatus.REJECTED
    order.decided_at = datetime.utcnow()
    order.notes = body.notes
    db.commit()

    write_audit_log(
        db, current_user, "RELEASE_ORDER_REJECTED", "ReleaseOrder", order.id,
        data_before=before, data_after={"status": order.status},
        ip_address=request.client.host,
    )
    return {"message": "Order rejected.", "order_id": order_id}


@router.post("/{order_id}/override")
async def override_safety_lock(
    order_id: int,
    request: Request,
    body: OverrideRequest,
    current_user: User = Depends(require_director),
    db: Session = Depends(get_db),
):
    """
    Rule 1 — Safety Lock Override.
    Director only. Requires MFA code + mandatory written justification.
    Every override is permanently logged — cannot be deleted.
    """
    if not current_user.mfa_enabled or not current_user.mfa_secret:
        raise HTTPException(status_code=403, detail="MFA must be enabled for safety lock overrides.")

    if not verify_mfa_token(current_user.mfa_secret, body.mfa_code):
        raise HTTPException(status_code=401, detail="Invalid MFA code. Override denied.")

    if not body.justification or len(body.justification.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="A written justification of at least 20 characters is required for override."
        )

    order = db.query(ReleaseOrder).filter(ReleaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    before = {"status": order.status}
    order.status = OrderStatus.OVERRIDE_APPROVED
    order.approved_by_id = current_user.id
    order.decided_at = datetime.utcnow()
    order.is_override = "true"
    order.override_justification = body.justification
    order.override_mfa_verified = "true"
    db.commit()

    write_audit_log(
        db, current_user, "SAFETY_LOCK_OVERRIDE", "ReleaseOrder", order.id,
        data_before=before,
        data_after={"status": order.status, "override": True},
        extra_notes=f"JUSTIFICATION: {body.justification}",
        ip_address=request.client.host,
    )

    return {"message": "Safety lock overridden. Release approved.", "order_id": order_id}


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    current_user: User = Depends(require_can_submit_order),
    db: Session = Depends(get_db),
):
    return db.query(ReleaseOrder).order_by(ReleaseOrder.requested_at.desc()).limit(100).all()
