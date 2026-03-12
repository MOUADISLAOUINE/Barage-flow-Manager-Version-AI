import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, BigInteger, Date, ForeignKey, Float, Text
from sqlalchemy.orm import relationship, synonym
from app.database import Base

class ContractStatus(str, enum.Enum):
    ACTIVE = "actif"
    SUSPENDED = "suspendu"
    EXPIRED = "expire"



class Contrat(Base):
    __tablename__ = "contrat"
    id_contrat = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = synonym("id_contrat")
    id_cooperative = Column(Integer, ForeignKey("cooperative.id_cooperative"), nullable=True)
    cooperative_id = synonym("id_cooperative")
    id_barrage = Column(Integer, ForeignKey("barrage.id_barrage"), nullable=True)
    dam_id = synonym("id_barrage")
    saison = Column(String(100), nullable=False)
    season = synonym("saison")
    volume_contracte_m3 = Column(BigInteger, nullable=False)
    contracted_volume_m3 = synonym("volume_contracte_m3")
    poids_priorite = Column(DECIMAL, nullable=False) # 'A=1.5 | B=1.0 | C=0.6'
    priority_weight = synonym("poids_priorite")
    statut = Column(String(50), nullable=False) # 'actif | expire | suspendu'
    status = synonym("statut")
    date_debut = Column(Date, nullable=True)
    season_start = synonym("date_debut")
    date_fin = Column(Date, nullable=True)
    season_end = synonym("date_fin")

    effective_allocation_m3 = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    cooperative = relationship("Cooperative", back_populates="contrats")
    barrage = relationship("Barrage", back_populates="contrats")
    dam = synonym("barrage")

Contract = Contrat
