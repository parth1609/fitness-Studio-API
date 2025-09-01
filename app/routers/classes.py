"""Class management routes.

Implements creation of fitness classes (auth required). Listing will be added in
subsequent tasks to keep commits aligned to the TODO plan.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models import FitnessClass, User
from app.schemas import ClassCreate, ClassOut
from app.utils.time import normalize_to_ist, is_past_in_ist

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("", response_model=ClassOut, status_code=status.HTTP_201_CREATED)
def create_class(
    class_in: ClassCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ClassOut:
    """Create a new fitness class.

    Authentication is required. Stores the scheduled time in IST timezone and
    rejects past date-times.
    """
    dt_ist = normalize_to_ist(class_in.date_time)
    if is_past_in_ist(dt_ist):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Class time cannot be in the past")
    item = FitnessClass(
        name=class_in.name,
        date_time=dt_ist,
        instructor=class_in.instructor,
        available_slots=class_in.available_slots,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


