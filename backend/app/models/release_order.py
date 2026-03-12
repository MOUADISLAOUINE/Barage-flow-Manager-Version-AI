from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship, synonym
from app.database import Base
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "EN_ATTENTE"
    APPROVED = "APPROUVE"
    REJECTED = "REJETE"
    BLOCKED = "BLOQUE"
    COMPLETED = "COMPLETE"
    OVERRIDE_APPROVED = "OVERRIDE_APPROVED"



class OrdreLiberation(Base):
    __tablename__ = "ordre_liberation"
    id_ordre = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = synonym("id_ordre")
    id_demandeur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=True)
    requested_by_id = synonym("id_demandeur")
    id_approbateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=True)
    approved_by_id = synonym("id_approbateur")
    id_cooperative = Column(Integer, ForeignKey("cooperative.id_cooperative"), nullable=True)
    cooperative_id = synonym("id_cooperative")
    
    dam_id = Column(Integer, ForeignKey("barrage.id_barrage"), nullable=True)
    
    volume_m3 = Column(BigInteger, nullable=False)
    timestamp_demande = Column(DateTime, nullable=False)
    requested_at = synonym("timestamp_demande")
    timestamp_decision = Column(DateTime, nullable=True)
    decided_at = synonym("timestamp_decision")
    statut = Column(String(50), nullable=False) # 'EN_ATTENTE | APPROUVE | REJETE | BLOQUE | COMPLETE'
    status = synonym("statut")
    notes_approbation = Column(Text, nullable=True)
    notes = synonym("notes_approbation")
    raison_blocage = Column(Text, nullable=True)
    
    # Missing fields for English backend compatibility
    is_override = Column(String(5), default="false")
    override_justification = Column(Text, nullable=True)
    override_mfa_verified = Column(String(5), default="false")
    ai_recommendation = Column(Text, nullable=True)
    scheduled_release_at = Column(DateTime, nullable=True)

    demandeur = relationship("Utilisateur", foreign_keys=[id_demandeur], back_populates="ordres_demandes")
    approbateur = relationship("Utilisateur", foreign_keys=[id_approbateur], back_populates="ordres_approuves")
    cooperative = relationship("Cooperative", back_populates="ordres_liberation")

ReleaseOrder = OrdreLiberation
