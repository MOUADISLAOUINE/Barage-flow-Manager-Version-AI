"""
core/security.py — Password hashing and TOTP MFA helpers
"""
import pyotp
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_mfa_secret() -> str:
    """Generate a new TOTP secret for a user."""
    return pyotp.random_base32()


def get_mfa_uri(secret: str, email: str, issuer: str = "BarrageFlowManager") -> str:
    """Return the otpauth URI for QR code generation."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=issuer)


def verify_mfa_token(secret: str, token: str) -> bool:
    """Verify a 6-digit TOTP code against the user's secret."""
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)
