"""Booking routes.

Defines endpoints for booking classes and listing user bookings.
Initial commit provides the router scaffold; endpoints will be added next.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models import Booking, FitnessClass, User
from app.schemas import BookingCreate, BookingOut
from app.utils.time import now_ist, normalize_to_ist

router = APIRouter(tags=["bookings"]) 


@router.post("/book", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def book_class(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BookingOut:
    """Book a class for the authenticated user.

    Validations:
    - Class must exist and must not be in the past.
    - Class must have available slots.
    - The same user cannot book the same class twice.
    Side effects: decrements the class's available_slots on success.
    """
    klass = db.query(FitnessClass).filter(FitnessClass.id == booking_in.class_id).first()
    if not klass:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    # Normalize to IST to guarantee offset-aware comparison against now_ist()
    if normalize_to_ist(klass.date_time) < now_ist():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot book a past class")

    if klass.available_slots <= 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No available slots")

    existing = (
        db.query(Booking)
        .filter(Booking.user_id == user.id, Booking.class_id == booking_in.class_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already booked for this class")

    booking = Booking(
        user_id=user.id,
        class_id=booking_in.class_id,
        client_name=booking_in.client_name,
        client_email=booking_in.client_email,
    )

    klass.available_slots -= 1
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/bookings", response_model=list[BookingOut])
def list_my_bookings(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[BookingOut]:
    """Return all bookings for the authenticated user (most recent first)."""
    items = (
        db.query(Booking)
        .filter(Booking.user_id == user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return items
