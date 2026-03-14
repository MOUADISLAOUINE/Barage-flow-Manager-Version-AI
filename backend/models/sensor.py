from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class SensorType(str, enum.Enum):
    level = "level"
    flow = "flow"
    rainfall = "rainfall"
    gate = "gate"


class SensorStatus(str, enum.Enum):
    OK = "OK"
    FAULT = "FAULT"
    OFFLINE = "OFFLINE"


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)

    dam_id = Column(Integer, ForeignKey("dams.id"))

    type = Column(Enum(SensorType), nullable=False)

    location_label = Column(String)

    unit = Column(String)

    status = Column(Enum(SensorStatus), default=SensorStatus.OK)

    last_calibration = Column(DateTime)

    dam = relationship("Dam")