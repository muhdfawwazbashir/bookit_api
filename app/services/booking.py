from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import uuid

from app.models.booking import Booking, BookingStatus
from app.schemas.booking import BookingCreate, BookingUpdate
from app.repositories import booking as booking_repo


def create_booking(db: Session, user_id: uuid.UUID, booking_data: BookingCreate) -> Booking:
    # check for overlapping booking
    conflict = booking_repo.find_overlapping_booking_for_service(
        db, booking_data.service_id, booking_data.start_time, booking_data.end_time
    )
    if conflict:
        raise HTTPException(
            status_code=400,
            detail="Booking conflict: service already booked for this time.",
        )

    new_booking = Booking(
        user_id=user_id,
        service_id=booking_data.service_id,
        start_time=booking_data.start_time,
        end_time=booking_data.end_time,
        status=BookingStatus.pending,
    )

    return booking_repo.create_booking(db, new_booking)

def get_booking(db: Session, booking_id: uuid.UUID, current_user, is_admin: bool = False) -> Booking:
    booking = booking_repo.get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if not is_admin and booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this booking")

    return booking

def get_bookings(db: Session, current_user, is_admin: bool = False,
                 status: str = None, start: datetime = None, end: datetime = None):
    if is_admin:
        return booking_repo.get_all_bookings(db, status=status, start=start, end=end)
    else:
        return booking_repo.get_bookings_by_user(db, current_user.id)

def update_booking(db: Session, booking_id: uuid.UUID, booking_update: BookingUpdate, current_user) -> Booking:
    booking = booking_repo.get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking_update.start_time:
        booking.start_time = booking_update.start_time
    if booking_update.end_time:
        booking.end_time = booking_update.end_time
    if booking_update.status:
        booking.status = booking_update.status

    return booking_repo.update_booking(db, booking)
def delete_booking(db: Session, booking_id: uuid.UUID, current_user, is_admin: bool = False) -> dict:
    booking = booking_repo.get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # user can only delete their own booking before it starts
    if not is_admin:
        if booking.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this booking")
        if booking.start_time <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="Cannot delete booking after it has started")

    booking_repo.delete_booking(db, booking)
    return {"detail": "Booking deleted successfully"}


# # Create booking (user)
# def create_booking(db: Session, user_id: str, booking_data: BookingCreate):
#     # check overlap for the same service
#     overlap = db.query(Booking).filter(
#         Booking.service_id == booking_data.service_id,
#         Booking.start_time < booking_data.end_time,
#         Booking.end_time > booking_data.start_time,
#         Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed])
#     ).first()

#     if overlap:
#         raise HTTPException(status_code=400, detail="Booking conflict: service already booked for this time")

#     booking = Booking(
#         user_id=user_id,
#         service_id=booking_data.service_id,
#         start_time=booking_data.start_time,
#         end_time=booking_data.end_time,
#         status=BookingStatus.pending
#     )
#     db.add(booking)
#     db.commit()
#     db.refresh(booking)
#     return booking


# # Get all bookings (admin: all, user: only theirs)
# def get_bookings(db: Session, user_id: str, is_admin: bool, status: str = None, start: datetime = None, end: datetime = None):
#     query = db.query(Booking)
    
#     if not is_admin:
#         query = query.filter(Booking.user_id == user_id)

#     if status:
#         query = query.filter(Booking.status == status)

#     if start:
#         query = query.filter(Booking.start_time >= start)

#     if end:
#         query = query.filter(Booking.end_time <= end)

#     return query.all()


# # Get booking by ID (owner or admin)
# def get_booking(db: Session, booking_id: str, user_id: str, is_admin: bool):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()
#     if not booking:
#         raise HTTPException(status_code=404, detail="Booking not found")
#     if not is_admin and booking.user_id != user_id:
#         raise HTTPException(status_code=403, detail="Not authorized to view this booking")
#     return booking


# # Update booking (owner: only if pending/confirmed, admin: any status)
# def update_booking(db: Session, booking_id: str, booking_update: BookingUpdate, user_id: str, is_admin: bool):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()
#     if not booking:
#         raise HTTPException(status_code=404, detail="Booking not found")

#     if not is_admin:
#         if booking.user_id != user_id:
#             raise HTTPException(status_code=403, detail="Not authorized to update this booking")
#         if booking.status not in [BookingStatus.pending, BookingStatus.confirmed]:
#             raise HTTPException(status_code=400, detail="Cannot update booking in its current status")

#     for key, value in booking_update.dict(exclude_unset=True).items():
#         setattr(booking, key, value)

#     db.commit()
#     db.refresh(booking)
#     return booking


# # Delete booking (owner: only before start_time, admin: anytime)
# def delete_booking(db: Session, booking_id: str, user_id: str, is_admin: bool):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()
#     if not booking:
#         raise HTTPException(status_code=404, detail="Booking not found")

#     if not is_admin:
#         if booking.user_id != user_id:
#             raise HTTPException(status_code=403, detail="Not authorized to delete this booking")
#         if booking.start_time <= datetime.utcnow():
#             raise HTTPException(status_code=400, detail="Cannot delete a booking that has already started")

#     db.delete(booking)
#     db.commit()
#     return {"detail": "Booking deleted successfully"}