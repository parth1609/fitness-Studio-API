"""Password hashing and verification utilities.

Provides a thin wrapper around Passlib's bcrypt password hashing for secure
storage of user passwords.

Functions
---------
- get_password_hash(password): Return a bcrypt hash of the given password.
- verify_password(plain_password, hashed_password): Verify a password against a
  previously stored hash.
"""
from __future__ import annotations

from passlib.context import CryptContext

# Bcrypt context for hashing and verification
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Return a bcrypt hash of ``password``.

    Parameters
    ----------
    password : str
        Plain text password to hash.

    Returns
    -------
    str
        Bcrypt hash suitable for storage.
    """
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check that ``plain_password`` matches ``hashed_password``.

    Parameters
    ----------
    plain_password : str
        User-provided plain text password.
    hashed_password : str
        Stored bcrypt hash to verify against.

    Returns
    -------
    bool
        True if the password is valid, False otherwise.
    """
    return _pwd_context.verify(plain_password, hashed_password)
