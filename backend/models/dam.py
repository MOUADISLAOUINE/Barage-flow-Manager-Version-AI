from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Dam(Base):
    __tablename__ = "dams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    gps_lat = Column(Float)
    gps_lng = Column(Float)

    max_capacity_m3 = Column(Float, nullable=False)

    # IMPORTANT: configurable threshold
    safety_threshold_pct = Column(Float, nullable=False)

    current_level_pct = Column(Float, default=0)

    zone = Column(String, default="NORMAL")

    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())