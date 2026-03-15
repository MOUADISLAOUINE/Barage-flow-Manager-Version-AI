"""
Authentication dependencies for FastAPI routes.
Provides `get_current_user` and `get_current_active_user`.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserStatus
from app.models.session import Session as DBSession
from app.core import security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Validate JWT and return the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = security.decode_token(token)
    if payload is None:
        raise credentials_exception
        
    user_id: str = payload.get("sub")
    jti: str = payload.get("jti")
    if user_id is None or jti is None:
        raise credentials_exception
        
    # Check if session exists and is not expired (i.e. not logged out / blacklisted)
    db_session = db.query(DBSession).filter(DBSession.jwt_jti == jti).first()
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
        )
    if db_session.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
        )
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
        
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure the user account is not suspended."""
    if current_user.status != UserStatus.ACTIVE.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Inactive or suspended user account"
        )
    return current_user
