from pydantic import BaseModel
from typing import Optional


# ── Password Validation ─────────────────────────────────────────────
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str


class MFAVerifyRequest(BaseModel):
    totp_code: str


class MFATokenResponse(BaseModel):
    mfa_verified_token: str
    expires_in_minutes: int
