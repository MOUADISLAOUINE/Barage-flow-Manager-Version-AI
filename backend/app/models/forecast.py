import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship, synonym
from app.database import Base

class ResultatPrevision(Base):
    __tablename__ = "resultat_prevision"
    id_prevision = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = synonym("id_prevision")
    id_barrage = Column(Integer, ForeignKey("barrage.id_barrage"), nullable=True)
    dam_id = synonym("id_barrage")
    date_generation = Column(DateTime, nullable=False)
    generated_at = synonym("date_generation")
    version_modele = Column(String(100), nullable=True)
    model_version = synonym("version_modele")
    niveaux_predits_json = Column(JSON, nullable=True)
    intervalles_confiance_json = Column(JSON, nullable=True)
    score_precision = Column(DECIMAL, nullable=True)
    mae_score = synonym("score_precision")
    horizon_jours = Column(Integer, nullable=True)
    
    # Missing fields
    forecast_data = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)

    barrage = relationship("Barrage", back_populates="previsions")

ForecastResult = ResultatPrevision
