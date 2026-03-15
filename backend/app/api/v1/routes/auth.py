"""
Authentication endpoints.
- POST /login: Issue JWT + Refresh Token
- POST /mfa/verify: Issue scoped MFA override token
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.core import security, auth
from app.models.user import User, UserRole
from app.models.session import Session as DBSession
from app.models.audit_log import AuditLog
from app.schemas.auth import LoginRequest, TokenResponse, MFAVerifyRequest, MFATokenResponse
from app.core.auth import oauth2_scheme

router = APIRouter(tags=["Auth"])


def log_audit_event(
    db: Session, 
    action: str, 
    user: User = None, 
    ip: str = None, 
    session_id: str = None, 
    target_entity: str = None, 
    target_id: int = None
):
    """Helper to write to the AuditLog"""
    log_entry = AuditLog(
        action=action,
        user_id=user.id if user else None,
        user_name=user.name if user else None,
        user_role=user.role if user else None,
        ip_address=ip,
        session_id=session_id,
        entity_name=target_entity,
        entity_id=target_id,
    )
    db.add(log_entry)
    db.commit()


@router.post("/login", response_model=TokenResponse)
def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT + Refresh Token. Logs the event."""
    user = db.query(User).filter(User.email == login_data.email).first()
    
    ip_address = request.client.host if request.client else None
    
    if not user or not security.verify_password(login_data.password, user.password_hash):
        log_audit_event(db, "FAILED_LOGIN_ATTEMPT", user=user, ip=ip_address, target_entity="User")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
        
    if user.status != "active":
        log_audit_event(db, "FAILED_LOGIN_SUSPENDED", user=user, ip=ip_address, target_entity="User", target_id=user.id)
        raise HTTPException(status_code=403, detail="Account suspended")

    # Generate tokens
    access_token, access_jti, access_exp = security.create_access_token(user.id, user.role)
    refresh_token, refresh_jti, refresh_exp = security.create_refresh_token(user.id)
    
    # Store access session in DB (for tracking/blacklisting)
    db_session = DBSession(
        user_id=user.id,
        jwt_jti=access_jti,
        expires_at=access_exp,
        ip_address=ip_address
    )
    db.add(db_session)
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Log successful login
    log_audit_event(db, "USER_LOGIN", user=user, ip=ip_address, session_id=access_jti, target_entity="User", target_id=user.id)

    return {
        "access_token": access_token if isinstance(access_token, str) else access_token.decode("utf-8"),
        "refresh_token": refresh_token if isinstance(refresh_token, str) else refresh_token.decode("utf-8"),
        "token_type": "bearer"
    }


@router.post("/mfa/verify", response_model=MFATokenResponse)
def verify_mfa(
    request: Request,
    mfa_data: MFAVerifyRequest, 
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Director-only endpoint. Validates TOTP code against user's mfa_secret.
    If valid, issues a short-lived 'mfa_verified' token scoped for override actions.
    """
    if current_user.role != UserRole.DIRECTOR.value:
        raise HTTPException(status_code=403, detail="MFA override tokens are only for Directors")
        
    if not current_user.mfa_enabled or not current_user.mfa_secret:
        raise HTTPException(status_code=400, detail="MFA is not enabled for this user")
        
    ip_address = request.client.host if request.client else None
        
    if not security.verify_mfa_code(current_user.mfa_secret, mfa_data.totp_code):
        log_audit_event(db, "FAILED_MFA_ATTEMPT", user=current_user, ip=ip_address, target_entity="User", target_id=current_user.id)
        raise HTTPException(status_code=401, detail="Invalid MFA code")

    # Generate 10-minute MFA scoped JWT token
    mfa_token, mfa_jti, mfa_exp = security.create_mfa_token(current_user.id)
    
    log_audit_event(db, "SUCCESSFUL_MFA_VERIFICATION", user=current_user, ip=ip_address, session_id=mfa_jti, target_entity="User", target_id=current_user.id)
    
    return {
        "mfa_verified_token": mfa_token,
        "expires_in_minutes": 10
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    request: Request,
    current_user: User = Depends(auth.get_current_active_user),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Logout the current user.
    Reads the JWT from the request, finds the matching session in the DB via 'jti',
    and sets its expires_at to now, effectively blacklisting it immediately.
    """
    payload = security.decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
    jti = payload.get("jti")
    
    # Invalidate session in DB
    db_session = db.query(DBSession).filter(DBSession.jwt_jti == jti).first()
    if db_session:
        # Expire right now
        db_session.expires_at = datetime.utcnow()
        db.commit()

    ip_address = request.client.host if request.client else None
    log_audit_event(
        db, 
        action="USER_LOGOUT", 
        user=current_user, 
        ip=ip_address, 
        session_id=jti,
        target_entity="Session", 
        target_id=db_session.id if db_session else None
    )

    return {"detail": "Successfully logged out"}
