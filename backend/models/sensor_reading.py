from sqlalchemy import Column, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class QualityFlag(str, enum.Enum):
    real = "real"
    estimated = "estimated"
    faulty = "faulty"


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)

    sensor_id = Column(Integer, ForeignKey("sensors.id"))

    timestamp = Column(DateTime, nullable=False)

    value = Column(Float, nullable=False)

    quality_flag = Column(Enum(QualityFlag), default=QualityFlag.real)

    sensor = relationship("Sensor")