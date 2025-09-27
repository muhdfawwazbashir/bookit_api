from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
import uuid

from app.models.booking import Booking, BookingStatus
from app.schemas.booking import BookingUpdate


def create_booking(db: Session, booking: Booking) -> Booking:
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking

def get_booking(db: Session, booking_id: uuid.UUID):
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_user_booking(db: Session, booking_id: uuid.UUID, user_id: uuid.UUID):
    return (
        db.query(Booking)
        .filter(Booking.id == booking_id, Booking.user_id == user_id)
        .first()
    )

def get_booking_by_id(db: Session, booking_id: uuid.UUID) -> Optional[Booking]:
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings_by_user(db: Session, user_id: uuid.UUID) -> List[Booking]:
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def get_all_bookings(
        db: Session,
        status: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
) -> List[Booking]:
    query = db.query(Booking)
    if status:
        query = query.filter(Booking.status == status)
    if start:
        query = query.filter(Booking.start_time >= start)
    if end:
        query = query.filter(Booking.end_time <= end)
    return query.all()

def get_bookings_by_service(db: Session, service_id: uuid.UUID) -> List[Booking]:
    return db.query(Booking).filter(Booking.service_id == service_id).all()

def find_overlapping_booking_for_service(
    db: Session,
    service_id: uuid.UUID,
    start_time: datetime,
    end_time: datetime,
) -> Optional[Booking]:
    return (
        db.query(Booking)
        .filter(
            Booking.service_id == service_id,
            Booking.start_time < end_time,
            Booking.end_time > start_time,
            Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
        )
        .first()
    )

def update_booking(db: Session, booking: Booking) -> Booking:
    db.commit()
    db.refresh(booking)
    return booking

    update_data = booking_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)
    return booking

def delete_booking(db: Session, booking: Booking) -> None:
    db.delete(booking)
    db.commit()