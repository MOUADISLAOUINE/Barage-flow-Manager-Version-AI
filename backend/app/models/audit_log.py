import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship, synonym
from app.database import Base

class JournalAudit(Base):
    __tablename__ = "journal_audit"
    id_log = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    id = synonym("id_log")
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=True)
    user_id = synonym("id_utilisateur")
    action = Column(String(100), nullable=False) # Changed from 200 based on typical schema habits
    entite_concernee = Column(String(200), nullable=True)
    resource_type = synonym("entite_concernee")
    id_entite = Column(Integer, nullable=True)
    resource_id = synonym("id_entite")
    donnees_avant_json = Column(JSON, nullable=True)
    data_before = synonym("donnees_avant_json")
    donnees_apres_json = Column(JSON, nullable=True)
    data_after = synonym("donnees_apres_json")
    timestamp = Column(DateTime, nullable=False)
    adresse_ip = Column(String(100), nullable=True)
    ip_address = synonym("adresse_ip")
    id_session = Column(String(200), nullable=True)
    session_id = synonym("id_session")
    
    # Missing fields
    user_name = Column(String(200), nullable=True)
    user_role = Column(String(50), nullable=True)
    extra_notes = Column(Text, nullable=True)

    utilisateur = relationship("Utilisateur", back_populates="logs_audit")

AuditLog = JournalAudit
