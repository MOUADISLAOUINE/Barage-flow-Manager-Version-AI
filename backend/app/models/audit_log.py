"""
AuditLog model — maps to the 'journal_audit' table.
Tracks all significant system actions.
"""

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class AuditLog(Base):
    __tablename__ = "journal_audit"

    id = Column("id_log", BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column("id_utilisateur", Integer, ForeignKey("utilisateur.id_utilisateur", ondelete="SET NULL"), nullable=True)
    action = Column("action", String(100), nullable=False)
    entity_name = Column("entite_concernee", String(200), nullable=True)
    entity_id = Column("id_entite", Integer, nullable=True)
    data_before = Column("donnees_avant_json", JSON, nullable=True)
    data_after = Column("donnees_apres_json", JSON, nullable=True)
    timestamp = Column("timestamp", DateTime, default=func.now(), nullable=False)
    ip_address = Column("adresse_ip", String(100), nullable=True)
    session_id = Column("id_session", String(200), nullable=True)
    
    # Ad-hoc denormalized columns for quick filtering (added in e41a5e35523b)
    user_name = Column("user_name", String(200), nullable=True)
    user_role = Column("user_role", String(50), nullable=True)
    extra_notes = Column("extra_notes", Text, nullable=True)

    # ── Relationship ────────────────────────────────────────────────
    user = relationship("User")

    def __repr__(self) -> str:
        return f"<AuditLog {self.id} action={self.action} user_id={self.user_id}>"
