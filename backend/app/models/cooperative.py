import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class PriorityClass(str, enum.Enum):
    A = "A"  # Food security crops — weight 1.5
    B = "B"  # Commercial crops   — weight 1.0
    C = "C"  # Other              — weight 0.6


class ContractStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    EXPIRED = "EXPIRED"


class Cooperative(Base):
    __tablename__ = "cooperatives"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    region = Column(String(200), nullable=False)
    land_area_hectares = Column(Float, nullable=False)
    crop_types = Column(String(500))
    priority_class = Column(Enum(PriorityClass), nullable=False, default=PriorityClass.B)
    contact_person = Column(String(200))
    contact_email = Column(String(200))
    contact_phone = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    contracts = relationship("Contract", back_populates="cooperative")


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"), nullable=False)
    dam_id = Column(Integer, ForeignKey("dams.id"), nullable=False)
    season = Column(String(50), nullable=False)  # e.g. "Summer 2025"
    season_start = Column(DateTime, nullable=False)
    season_end = Column(DateTime, nullable=False)
    contracted_volume_m3 = Column(Float, nullable=False)
    # Current effective allocation after zone-based reductions
    effective_allocation_m3 = Column(Float, nullable=False)
    priority_weight = Column(Float, nullable=False, default=1.0)
    status = Column(Enum(ContractStatus), default=ContractStatus.ACTIVE)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cooperative = relationship("Cooperative", back_populates="contracts")
    dam = relationship("Dam", back_populates="contracts")
