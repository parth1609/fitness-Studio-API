"""Database session and engine configuration.

Creates the SQLAlchemy engine, session factory, and declarative base. Uses the
configuration from ``app.core.config.settings``. For SQLite, sets
``check_same_thread=False`` to allow using the same connection across threads in
FastAPI.
"""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """Base class for all ORM models."""


# SQLite needs check_same_thread=False when used with FastAPI/Uvicorn
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
