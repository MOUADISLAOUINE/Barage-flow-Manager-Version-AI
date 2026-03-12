from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Float, Boolean
from sqlalchemy.orm import relationship, synonym
from app.database import Base
import enum

class WaterZone(str, enum.Enum):
    NORMAL = "NORMAL"
    ALERT = "ALERT"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class SensorType(str, enum.Enum):
    LEVEL = "niveau"
    FLOW = "debit"
    RAINFALL = "pluie"
    GATE = "vanne"

class SensorStatus(str, enum.Enum):
    OK = "OK"
    FAULT = "PANNE"
    OFFLINE = "HORS_LIGNE"

class ReadingQuality(str, enum.Enum):
    REAL = "reel"
    ESTIMATED = "estime"
    FAULTY = "defectueux"

class Barrage(Base):
    __tablename__ = "barrage"
    id_barrage = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = synonym("id_barrage")
    nom = Column(String(200), nullable=True)
    name = synonym("nom")
    localisation_gps = Column(String(300), nullable=True)
    location = synonym("localisation_gps")
    capacite_max_m3 = Column(BigInteger, nullable=True)
    max_capacity_m3 = synonym("capacite_max_m3")
    seuil_reserve_m3 = Column(BigInteger, nullable=True)
    
    # Missing fields for English code compatibility
    safety_reserve_pct = Column(Float, nullable=False, default=25.0)
    current_level_m3 = synonym("niveau_actuel_m3")
    current_level_pct = Column(Float, nullable=False, default=0.0)
    safety_lock_active = Column(Boolean, default=False)
    current_zone = Column(String(50), default="NORMAL") # Maps to WaterZone string

    niveau_actuel_m3 = Column(BigInteger, nullable=True)
    derniere_maj = Column(DateTime, nullable=True)
    last_reading_at = synonym("derniere_maj")

    capteurs = relationship("Capteur", back_populates="barrage")
    sensors = synonym("capteurs")
    contrats = relationship("Contrat", back_populates="barrage")
    contracts = synonym("contrats")
    previsions = relationship("ResultatPrevision", back_populates="barrage")

Dam = Barrage
