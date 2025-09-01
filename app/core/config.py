"""Application configuration settings.

Provides central configuration for secrets, database URL, and other tunables.
Reads values from environment variables with sensible defaults for local
SQLite development. This avoids hardcoding secrets in code and eases
configuration in different environments.

Environment variables
---------------------
- SECRET_KEY: JWT signing secret. A random string in production.
- ALGORITHM: JWT algorithm (default: HS256).
- ACCESS_TOKEN_EXPIRE_MINUTES: JWT access token expiry in minutes (default: 60).
- DATABASE_URL: SQLAlchemy URL (default: sqlite:///./db.sqlite3).
- CORS_ORIGINS: Comma-separated list of allowed origins (default: *).
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Container for application settings.

    Attributes
    ----------
    SECRET_KEY : str
        Secret used to sign JWTs. Do NOT commit real secrets.
    ALGORITHM : str
        Signing algorithm for JWTs (e.g., HS256).
    ACCESS_TOKEN_EXPIRE_MINUTES : int
        Expiration time for access tokens in minutes.
    DATABASE_URL : str
        SQLAlchemy database URI.
    CORS_ORIGINS : list[str]
        List of allowed CORS origins for local development.
    """

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
    CORS_ORIGINS: list[str] = (
        os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") else ["*"]
    )


settings = Settings()
