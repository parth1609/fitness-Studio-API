"""JWT helper utilities for access token creation and validation.

Uses HS256 signing with a configurable secret key. Tokens carry a standard
"sub" (subject) claim, which we use to encode the authenticated user's ID.

Functions
---------
- create_access_token(subject, expires_delta): Create a signed JWT.
- decode_token(token): Decode and validate a JWT, returning the payload.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(
    subject: Union[str, int], *, expires_delta: Optional[timedelta] = None, extra_claims: Optional[Dict[str, Any]] = None
) -> str:
    """Create a signed JWT access token.

    Parameters
    ----------
    subject : str | int
        The token subject, typically the user ID.
    expires_delta : timedelta, optional
        Time delta until expiration. Defaults to settings.ACCESS_TOKEN_EXPIRE_MINUTES.
    extra_claims : dict, optional
        Extra claims to include in the token payload.

    Returns
    -------
    str
        Encoded JWT string.
    """
    now = datetime.now(tz=timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode: Dict[str, Any] = {"sub": str(subject), "iat": int(now.timestamp()), "exp": int(expire.timestamp())}
    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT, returning its payload.

    Parameters
    ----------
    token : str
        Encoded JWT to validate.

    Returns
    -------
    dict
        Decoded payload containing at least the "sub" claim.

    Raises
    ------
    jose.JWTError
        If the token is invalid or expired.
    """
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload
