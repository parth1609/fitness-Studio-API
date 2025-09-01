"""Authentication routes: signup and (later) login.

This module currently implements the user signup endpoint. The login endpoint
will be added in the next task to keep commits aligned with the TODO plan.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.core.jwt import create_access_token
from app.dependencies import get_db
from app.models import User
from app.schemas import Login, Token, UserCreate, UserOut

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


@router.post("/login", response_model=Token)
def login(credentials: Login, db: Session = Depends(get_db)) -> Token:
    """Authenticate a user and issue a JWT access token.

    Returns 401 if the credentials are invalid. On success, returns a bearer
    token suitable for use in the Authorization header.
    """
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.id)
    return Token(access_token=token, token_type="bearer")
