import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Date, Float, BigInteger
from sqlalchemy.orm import relationship, synonym
from app.database import Base

class Capteur(Base):
    __tablename__ = "capteur"
    id_capteur = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id = synonym("id_capteur")
    id_barrage = Column(Integer, ForeignKey("barrage.id_barrage"), nullable=True)
    dam_id = synonym("id_barrage")
    name = Column(String(100), nullable=True) # missing in French schema but required by English code
    type_capteur = Column(String(50), nullable=False) # 'niveau | debit | pluie | vanne'
    sensor_type = synonym("type_capteur")
    localisation = Column(String(300), nullable=True)
    location_description = synonym("localisation")
    unite_mesure = Column(String(50), nullable=True)
    unit_of_measure = synonym("unite_mesure")
    statut = Column(String(50), nullable=False) # 'OK | PANNE | HORS_LIGNE'
    status = synonym("statut")
    derniere_calibration = Column(Date, nullable=True)
    last_calibration_date = synonym("derniere_calibration")

    barrage = relationship("Barrage", back_populates="capteurs")
    dam = synonym("barrage")
    lectures = relationship("LectureCapteur", back_populates="capteur")
    readings = synonym("lectures")

class LectureCapteur(Base):
    __tablename__ = "lecture_capteur"
    id_lecture = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id = synonym("id_lecture")
    id_capteur = Column(Integer, ForeignKey("capteur.id_capteur"), nullable=True)
    sensor_id = synonym("id_capteur")
    timestamp = Column(DateTime, nullable=False)
    recorded_at = synonym("timestamp")
    valeur = Column(DECIMAL, nullable=False)
    value = synonym("valeur")
    indicateur_qualite = Column(String(50), nullable=False) # 'reel | estime | defectueux'
    quality = synonym("indicateur_qualite")

    capteur = relationship("Capteur", back_populates="lectures")
    sensor = synonym("capteur")

Sensor = Capteur
SensorReading = LectureCapteur
