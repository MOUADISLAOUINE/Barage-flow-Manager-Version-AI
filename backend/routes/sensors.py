from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sensor import Sensor, SensorStatus, SensorType
from app.models.sensor_reading import SensorReading
from app.schemas.sensor_reading import SensorReadingCreate
from datetime import datetime

router = APIRouter()


@router.post("/api/v1/sensors/readings", status_code=201)
def ingest_sensor_reading(data: SensorReadingCreate, db: Session = Depends(get_db)):

    # 1️⃣ check if sensor exists
    sensor = db.query(Sensor).filter(Sensor.id == data.sensor_id).first()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    # 2️⃣ check sensor status
    if sensor.status == SensorStatus.OFFLINE:
        raise HTTPException(status_code=400, detail="Sensor is OFFLINE")

    # 3️⃣ validate physical range (example for level sensors)
    if sensor.type == SensorType.level:
        if data.value < 0 or data.value > 100:
            raise HTTPException(status_code=400, detail="Invalid level value")

    # 4️⃣ save reading
    reading = SensorReading(
        sensor_id=data.sensor_id,
        value=data.value,
        timestamp=data.timestamp
    )

    db.add(reading)
    db.commit()

    return {"message": "Sensor reading stored"}