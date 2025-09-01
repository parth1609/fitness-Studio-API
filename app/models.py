"""ORM models for the Fitness Studio Booking API.

Models:
- User: Registered application users.
- FitnessClass: Studio classes stored in IST time.
- Booking: Reservation of a user for a class.

Notes
-----
- Times are handled as timezone-aware datetimes. We convert inputs to IST
  before persisting. SQLite does not enforce timezone, but SQLAlchemy will
  keep offsets through Python objects.
- We prevent duplicate bookings via a unique constraint on (user_id, class_id).
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
    """Application user.

    Attributes
    ----------
    id : int
        Primary key.
    name : str
        Display name of the user.
    email : str
        Unique email used for login/identification.
    hashed_password : str
        Bcrypt-hashed password.
    created_at : datetime
        Server-side creation timestamp (UTC).
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    bookings: Mapped[list["Booking"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class FitnessClass(Base):
    """A fitness class offered by the studio.

    Attributes
    ----------
    id : int
        Primary key.
    name : str
        Class title.
    date_time : datetime
        Scheduled date-time stored in IST timezone.
    instructor : str
        Instructor's name.
    available_slots : int
        Remaining bookable slots.
    created_at, updated_at : datetime
        Timestamps managed by the database on insert/update.
    """

    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    instructor: Mapped[str] = mapped_column(String(100), nullable=False)
    available_slots: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    bookings: Mapped[list["Booking"]] = relationship(back_populates="fitness_class", cascade="all, delete-orphan")


class Booking(Base):
    """A user's booking for a class.

    Attributes
    ----------
    id : int
        Primary key.
    user_id : int
        FK to users.id.
    class_id : int
        FK to classes.id.
    client_name : str
        Name of the attendee (could match user's name).
    client_email : str
        Email of the attendee.
    created_at : datetime
        Server-side creation timestamp.
    """

    __tablename__ = "bookings"
    __table_args__ = (
        UniqueConstraint("user_id", "class_id", name="uq_booking_user_class"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=False, index=True)

    client_name: Mapped[str] = mapped_column(String(100), nullable=False)
    client_email: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="bookings")
    fitness_class: Mapped[FitnessClass] = relationship(back_populates="bookings")
