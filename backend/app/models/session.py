"""
Session & MFA Token models.

- Session:   Tracks active JWT tokens for blacklisting on logout.
- MFAToken:  Stores one-time TOTP codes for MFA verification.
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


# ── Session (JWT blacklist support) ─────────────────────────────────
class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateur.id_utilisateur", ondelete="CASCADE"), nullable=False, index=True)
    jwt_jti = Column(String(200), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # ── Relationship ────────────────────────────────────────────────
    user = relationship("User", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<Session user_id={self.user_id} jti={self.jwt_jti[:8]}...>"


# ── MFA Token (TOTP verification) ──────────────────────────────────
class MFAToken(Base):
    __tablename__ = "mfa_token"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateur.id_utilisateur", ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String(10), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # ── Relationship ────────────────────────────────────────────────
    user = relationship("User", back_populates="mfa_tokens")

    def __repr__(self) -> str:
        return f"<MFAToken user_id={self.user_id} used={self.used}>"
