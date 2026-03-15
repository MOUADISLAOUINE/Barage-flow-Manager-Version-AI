"""
User model — maps to the 'utilisateur' table.

Roles:   Director | Operator | Officer | Admin
Status:  active   | suspended
"""

import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


# ── Enums ───────────────────────────────────────────────────────────
class UserRole(str, enum.Enum):
    DIRECTOR = "Director"
    OPERATOR = "Operator"
    OFFICER = "Officer"
    ADMIN = "Admin"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


# ── Model ───────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "utilisateur"

    id = Column("id_utilisateur", Integer, primary_key=True, autoincrement=True, index=True)
    name = Column("nom", String(200))
    email = Column("email", String(200), unique=True, nullable=False, index=True)
    password_hash = Column("mot_de_passe_hash", String(300), nullable=False)
    role = Column(
        "role",
        String(50),
        nullable=False,
        index=True,
    )
    status = Column("statut", String(50), nullable=False, default=UserStatus.ACTIVE.value)
    last_login = Column("derniere_connexion", DateTime, nullable=True)
    mfa_enabled = Column("mfa_active", Boolean, nullable=False, default=False)
    mfa_secret = Column("sel_mfa", String(100), nullable=True)

    # ── Relationships ───────────────────────────────────────────────
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    mfa_tokens = relationship("MFAToken", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.id} {self.email} role={self.role}>"
