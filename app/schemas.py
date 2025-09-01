"""Pydantic schemas for request/response models.

Aligns API shapes to the assignment statement while following Pydantic v2
conventions. Field aliases are used to match the specified JSON keys such as
"dateTime" and "availableSlots".
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ----------------------
# Authentication schemas
# ----------------------
class UserCreate(BaseModel):
    """Schema for user signup requests."""

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserOut(BaseModel):
    """Public user shape returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    created_at: datetime


class Login(BaseModel):
    """Schema for login requests."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Access token response model."""

    access_token: str
    token_type: str = "bearer"


# -----------------
# Classes schemas
# -----------------
class ClassCreate(BaseModel):
    """Schema to create a new fitness class.

    Input alias names are used to match the statement's JSON format.
    """

    name: str = Field(min_length=1, max_length=150)
    date_time: datetime = Field(alias="dateTime")
    instructor: str = Field(min_length=1, max_length=100)
    available_slots: int = Field(alias="availableSlots", ge=1, le=100)

    model_config = ConfigDict(populate_by_name=True)


class ClassOut(BaseModel):
    """Public class representation with field aliases."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date_time: datetime = Field(alias="dateTime")
    instructor: str
    available_slots: int = Field(alias="availableSlots")


# -----------------
# Booking schemas
# -----------------
class BookingCreate(BaseModel):
    """Schema to book a class."""

    class_id: int
    client_name: str = Field(min_length=1, max_length=100)
    client_email: EmailStr


class BookingOut(BaseModel):
    """Public booking representation, optionally including class info."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    created_at: datetime

    # Optionally nested class details when returned by endpoints
    fitness_class: Optional[ClassOut] = None
