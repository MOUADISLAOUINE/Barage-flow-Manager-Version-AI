from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.database import get_db
from app.models.user import Utilisateur as User
from app.core.auth import create_access_token, get_current_active_user
from app.core.security import verify_password, verify_mfa_token
from app.services.audit_service import write_audit_log

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    mfa_required: bool = False


class MFAVerifyRequest(BaseModel):
    temp_token: str
    mfa_code: str


@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    if user.mfa_enabled:
        # Issue a short-lived temp token; client must complete MFA
        temp_token = create_access_token({"sub": str(user.id), "mfa_pending": True})
        return TokenResponse(
            access_token=temp_token,
            role=user.role.value,
            mfa_required=True,
        )

    # Full login
    user.last_login_at = datetime.utcnow()
    db.commit()

    write_audit_log(
        db, user, "USER_LOGIN", "User", user.id,
        ip_address=request.client.host,
    )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, role=user.role.value)


@router.post("/verify-mfa", response_model=TokenResponse)
async def verify_mfa(
    request: Request,
    body: MFAVerifyRequest,
    db: Session = Depends(get_db),
):
    """Second step: verify TOTP code after password login."""
    from jose import jwt, JWTError
    from app.config import settings

    try:
        payload = jwt.decode(body.temp_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if not payload.get("mfa_pending"):
            raise HTTPException(status_code=400, detail="Token is not an MFA pending token.")
        user_id = int(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not verify_mfa_token(user.mfa_secret, body.mfa_code):
        raise HTTPException(status_code=401, detail="Invalid MFA code.")

    user.last_login_at = datetime.utcnow()
    db.commit()

    write_audit_log(db, user, "USER_LOGIN_MFA", "User", user.id, ip_address=request.client.host)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, role=user.role.value)


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    write_audit_log(db, current_user, "USER_LOGOUT", "User", current_user.id,
                    ip_address=request.client.host)
    return {"message": "Logged out successfully."}
