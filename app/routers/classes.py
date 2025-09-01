"""Class management routes.

Implements creation of fitness classes (auth required). Listing will be added in
subsequent tasks to keep commits aligned to the TODO plan.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models import FitnessClass, User
from app.schemas import ClassCreate, ClassOut

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("", response_model=ClassOut, status_code=status.HTTP_201_CREATED)
def create_class(
    class_in: ClassCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ClassOut:
    """Create a new fitness class.

    Authentication is required. Initial implementation stores fields as-is; IST
    normalization and validation are added in subsequent tasks.
    """
    item = FitnessClass(
        name=class_in.name,
        date_time=class_in.date_time,
        instructor=class_in.instructor,
        available_slots=class_in.available_slots,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
