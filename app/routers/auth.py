"""Authentication routes: signup and (later) login.

This module currently implements the user signup endpoint. The login endpoint
will be added in the next task to keep commits aligned with the TODO plan.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate, UserOut

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    """Register a new user.

    Validates that the email is not already registered, hashes the password,
    and stores the user record.
    """
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
