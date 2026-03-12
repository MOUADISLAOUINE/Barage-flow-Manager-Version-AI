from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, synonym
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    DIRECTOR = "Directeur"
    OPERATOR = "Operateur"
    AGRICULTURAL_OFFICER = "Officier"
    ADMIN = "Admin"

class UserStatus(str, enum.Enum):
    ACTIVE = "actif"
    SUSPENDED = "suspendu"

class Utilisateur(Base):
    __tablename__ = "utilisateur"
    id_utilisateur = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = synonym("id_utilisateur")
    nom = Column(String(200), nullable=True)
    full_name = synonym("nom")
    email = Column(String(200), unique=True, nullable=False, index=True)
    mot_de_passe_hash = Column(String(300), nullable=False)
    hashed_password = synonym("mot_de_passe_hash")
    role = Column(String(50), nullable=False) # 'Directeur | Operateur | Officier | Admin'
    statut = Column(String(50), nullable=False) # 'actif | suspendu'
    status = synonym("statut")
    derniere_connexion = Column(DateTime, nullable=True)
    last_login_at = synonym("derniere_connexion")
    mfa_active = Column(Boolean, nullable=False, default=False)
    mfa_enabled = synonym("mfa_active")
    sel_mfa = Column(String(100), nullable=True)
    mfa_secret = synonym("sel_mfa")

    ordres_demandes = relationship("OrdreLiberation", foreign_keys="[OrdreLiberation.id_demandeur]", back_populates="demandeur")
    ordres_approuves = relationship("OrdreLiberation", foreign_keys="[OrdreLiberation.id_approbateur]", back_populates="approbateur")
    logs_audit = relationship("JournalAudit", back_populates="utilisateur")

User = Utilisateur
