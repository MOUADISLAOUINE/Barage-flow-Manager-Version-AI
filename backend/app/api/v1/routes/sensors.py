"""api/v1/routes/sensors.py"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.dam import Sensor, SensorReading, ReadingQuality
from app.core.rbac import require_water_access
from app.models.user import User
from app.services.dam_service import update_dam_level
from app.models.dam import Dam

router = APIRouter()


class SensorReadingIngest(BaseModel):
    sensor_id: int
    value: float
    recorded_at: datetime
    quality: ReadingQuality = ReadingQuality.REAL


@router.post("/readings", status_code=201)
async def ingest_sensor_reading(
    body: SensorReadingIngest,
    current_user: User = Depends(require_water_access),
    db: Session = Depends(get_db),
):
    sensor = db.query(Sensor).filter(Sensor.id == body.sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found.")

    reading = SensorReading(
        sensor_id=body.sensor_id,
        recorded_at=body.recorded_at,
        value=body.value,
        quality=body.quality,
    )
    db.add(reading)
    db.commit()

    # If this is a level sensor, update the dam state
    from app.models.dam import SensorType
    if sensor.sensor_type == SensorType.LEVEL:
        dam = db.query(Dam).filter(Dam.id == sensor.dam_id).first()
        if dam:
            update_dam_level(db, dam, body.value)

    return {"message": "Reading ingested.", "sensor_id": body.sensor_id}


@router.get("/")
async def list_sensors(
    dam_id: int = 1,
    current_user: User = Depends(require_water_access),
    db: Session = Depends(get_db),
):
    return db.query(Sensor).filter(Sensor.dam_id == dam_id).all()
