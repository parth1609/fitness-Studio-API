"""FastAPI dependency providers.

Includes database session management and the current user resolver based on
Bearer JWTs in the Authorization header.
"""
from __future__ import annotations

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.jwt import decode_token
from app.db.session import SessionLocal
from app.models import User


security_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the authenticated ``User`` from the Bearer token.

    Expects an ``Authorization: Bearer <token>`` header. On failure, raises
    401 Unauthorized with a WWW-Authenticate header per RFC6750.
    """
    if creds is None or not creds.scheme.lower() == "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_token(creds.credentials)
        subject = payload.get("sub")
        user_id = int(subject)
    except Exception:  # jose.JWTError or ValueError
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
