import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"       # Safety lock engaged
    COMPLETED = "COMPLETED"
    OVERRIDE_APPROVED = "OVERRIDE_APPROVED"  # Director MFA override


class ReleaseOrder(Base):
    __tablename__ = "release_orders"

    id = Column(Integer, primary_key=True, index=True)
    requested_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"), nullable=True)
    dam_id = Column(Integer, ForeignKey("dams.id"), nullable=False)

    volume_m3 = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True)

    # Override fields (Director MFA override)
    is_override = Column(String(5), default="false")
    override_justification = Column(Text, nullable=True)
    override_mfa_verified = Column(String(5), default="false")

    # AI recommendation attached to this order
    ai_recommendation = Column(Text, nullable=True)

    requested_at = Column(DateTime, default=datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)
    scheduled_release_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)


# ------------------------------------------------------------------
# AuditLog — APPEND ONLY, NEVER UPDATE OR DELETE
# ------------------------------------------------------------------
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    # Who
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    user_name = Column(String(200), nullable=False)   # Denormalised for immutability
    user_role = Column(String(50), nullable=False)

    # What
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False)  # e.g. "ReleaseOrder"
    resource_id = Column(Integer, nullable=True)

    # Before / After snapshot
    data_before = Column(JSON, nullable=True)
    data_after = Column(JSON, nullable=True)
    extra_notes = Column(Text, nullable=True)

    # When / Where
    timestamp = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    ip_address = Column(String(50), nullable=True)
    session_id = Column(String(100), nullable=True)

    # AuditLog is append-only — no update or delete operations exist for this model.


# ------------------------------------------------------------------
# ForecastResult
# ------------------------------------------------------------------
class ForecastResult(Base):
    __tablename__ = "forecast_results"

    id = Column(Integer, primary_key=True, index=True)
    dam_id = Column(Integer, ForeignKey("dams.id"), nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow, index=True)
    model_version = Column(String(50), nullable=False)
    # 180-day forecast as JSON list of {date, predicted_pct, lower_bound, upper_bound}
    forecast_data = Column(JSON, nullable=False)
    mae_score = Column(Float, nullable=True)   # Mean Absolute Error vs actuals
    notes = Column(Text, nullable=True)
