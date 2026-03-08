"""
models/dam.py — Dam & Sensor ORM models
"""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class WaterZone(str, enum.Enum):
    NORMAL = "NORMAL"       # > 60%
    ALERT = "ALERT"         # 40–60%
    WARNING = "WARNING"     # 25–40%
    CRITICAL = "CRITICAL"   # < 25%


class SensorType(str, enum.Enum):
    LEVEL = "LEVEL"
    FLOW = "FLOW"
    RAINFALL = "RAINFALL"
    GATE = "GATE"


class SensorStatus(str, enum.Enum):
    OK = "OK"
    FAULT = "FAULT"
    OFFLINE = "OFFLINE"


class ReadingQuality(str, enum.Enum):
    REAL = "REAL"
    ESTIMATED = "ESTIMATED"
    FAULTY = "FAULTY"


# ------------------------------------------------------------------
# Dam
# ------------------------------------------------------------------
class Dam(Base):
    __tablename__ = "dams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    location = Column(String(300), nullable=False)
    gps_lat = Column(Float, nullable=True)
    gps_lon = Column(Float, nullable=True)

    # Capacity (m³)
    max_capacity_m3 = Column(Float, nullable=False)          # e.g. ~296_000_000 m³
    current_level_m3 = Column(Float, nullable=False, default=0.0)
    current_level_pct = Column(Float, nullable=False, default=0.0)

    # Safety rules — NEVER hard-coded, always read from DB
    safety_reserve_pct = Column(Float, nullable=False, default=25.0)
    safety_lock_active = Column(Boolean, default=False)
    current_zone = Column(Enum(WaterZone), default=WaterZone.NORMAL)

    last_reading_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    sensors = relationship("Sensor", back_populates="dam")
    contracts = relationship("Contract", back_populates="dam")


# ------------------------------------------------------------------
# Sensor
# ------------------------------------------------------------------
class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    dam_id = Column(Integer, ForeignKey("dams.id"), nullable=False)
    name = Column(String(100), nullable=False)
    sensor_type = Column(Enum(SensorType), nullable=False)
    location_description = Column(String(300))
    unit_of_measure = Column(String(20))  # e.g. "m³", "m³/s", "mm", "open/closed"
    status = Column(Enum(SensorStatus), default=SensorStatus.OK)
    last_calibration_date = Column(DateTime, nullable=True)

    dam = relationship("Dam", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor")


# ------------------------------------------------------------------
# SensorReading — high-volume append-only table
# ------------------------------------------------------------------
class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False, index=True)
    recorded_at = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=False)
    quality = Column(Enum(ReadingQuality), default=ReadingQuality.REAL)

    sensor = relationship("Sensor", back_populates="readings")
