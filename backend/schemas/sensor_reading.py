from pydantic import BaseModel
from datetime import datetime


class SensorReadingCreate(BaseModel):
    sensor_id: int
    value: float
    timestamp: datetime