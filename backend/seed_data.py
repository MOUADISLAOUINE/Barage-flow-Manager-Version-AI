"""
seed_data.py — Populate the database with realistic development data.

Run: python seed_data.py
(inside the backend container or local venv)
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models import (
    Dam, Sensor, User, Cooperative, Contract,
    WaterZone, SensorType, SensorStatus, UserRole, PriorityClass, ContractStatus
)
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()


def seed():
    print("🌱 Seeding development database...")

    # ── Dam ──────────────────────────────────────────────────────────
    dam = Dam(
        name="Youssef Ibn Tachfine Dam",
        location="Tiznit, Souss-Massa, Morocco",
        gps_lat=29.8833,
        gps_lon=-9.7167,
        max_capacity_m3=296_000_000,
        current_level_m3=165_760_000,   # ~56% — Alert zone
        current_level_pct=56.0,
        safety_reserve_pct=25.0,
        safety_lock_active=False,
        current_zone=WaterZone.ALERT,
    )
    db.add(dam)
    db.flush()

    # ── Sensors ───────────────────────────────────────────────────────
    sensors = [
        Sensor(dam_id=dam.id, name="Main Level Gauge", sensor_type=SensorType.LEVEL,
               unit_of_measure="m³", status=SensorStatus.OK),
        Sensor(dam_id=dam.id, name="Outlet Flow Meter", sensor_type=SensorType.FLOW,
               unit_of_measure="m³/s", status=SensorStatus.OK),
        Sensor(dam_id=dam.id, name="Rain Gauge Station 1", sensor_type=SensorType.RAINFALL,
               unit_of_measure="mm", status=SensorStatus.OK),
        Sensor(dam_id=dam.id, name="Rain Gauge Station 3", sensor_type=SensorType.RAINFALL,
               unit_of_measure="mm", status=SensorStatus.FAULT),
        Sensor(dam_id=dam.id, name="Main Gate Position", sensor_type=SensorType.GATE,
               unit_of_measure="open/closed", status=SensorStatus.OK),
    ]
    for s in sensors:
        db.add(s)

    # ── Users ─────────────────────────────────────────────────────────
    users = [
        User(full_name="Hassan El Mansouri", email="director@barrage.ma",
             hashed_password=hash_password("director123!"),
             role=UserRole.DIRECTOR, mfa_enabled=False),
        User(full_name="Fatima Zahra Benali", email="operator1@barrage.ma",
             hashed_password=hash_password("operator123!"),
             role=UserRole.OPERATOR),
        User(full_name="Youssef Aït Brahim", email="operator2@barrage.ma",
             hashed_password=hash_password("operator123!"),
             role=UserRole.OPERATOR),
        User(full_name="Nadia Tazi", email="officer@barrage.ma",
             hashed_password=hash_password("officer123!"),
             role=UserRole.AGRICULTURAL_OFFICER),
        User(full_name="Karim Lahlou", email="admin@barrage.ma",
             hashed_password=hash_password("admin123!"),
             role=UserRole.ADMIN),
    ]
    for u in users:
        db.add(u)

    # ── Cooperatives ─────────────────────────────────────────────────
    coops = [
        Cooperative(name="Coopérative Ajdal", region="Tiznit Nord",
                    land_area_hectares=850, crop_types="Argan, Orge",
                    priority_class=PriorityClass.A,
                    contact_person="Mohamed Abargh", contact_email="ajdal@coops.ma"),
        Cooperative(name="Coopérative Tafraout", region="Tafraout",
                    land_area_hectares=620, crop_types="Blé, Maïs",
                    priority_class=PriorityClass.B,
                    contact_person="Aicha Idbassaid", contact_email="tafraout@coops.ma"),
        Cooperative(name="Coopérative Souss Vert", region="Tiznit Sud",
                    land_area_hectares=430, crop_types="Légumes",
                    priority_class=PriorityClass.C,
                    contact_person="Omar Chafai", contact_email="soussvert@coops.ma"),
    ]
    for c in coops:
        db.add(c)
    db.flush()

    # ── Contracts (Summer 2025 season) ────────────────────────────────
    season_start = datetime(2025, 6, 1)
    season_end = datetime(2025, 10, 31)
    contracts = [
        Contract(cooperative_id=coops[0].id, dam_id=dam.id,
                 season="Summer 2025", season_start=season_start, season_end=season_end,
                 contracted_volume_m3=620_000, effective_allocation_m3=558_000,
                 priority_weight=1.5, status=ContractStatus.ACTIVE),
        Contract(cooperative_id=coops[1].id, dam_id=dam.id,
                 season="Summer 2025", season_start=season_start, season_end=season_end,
                 contracted_volume_m3=450_000, effective_allocation_m3=405_000,
                 priority_weight=1.0, status=ContractStatus.ACTIVE),
        Contract(cooperative_id=coops[2].id, dam_id=dam.id,
                 season="Summer 2025", season_start=season_start, season_end=season_end,
                 contracted_volume_m3=280_000, effective_allocation_m3=252_000,
                 priority_weight=0.6, status=ContractStatus.ACTIVE),
    ]
    for ct in contracts:
        db.add(ct)

    db.commit()
    print("✅ Seed complete.")
    print("\n📋 Test credentials:")
    print("  Director:  director@barrage.ma  / director123!")
    print("  Operator:  operator1@barrage.ma / operator123!")
    print("  Officer:   officer@barrage.ma   / officer123!")
    print("  Admin:     admin@barrage.ma     / admin123!")


if __name__ == "__main__":
    seed()
    db.close()
