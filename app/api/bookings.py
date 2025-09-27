from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.schemas.booking import BookingCreate, BookingUpdate, BookingOut
from app.services import booking as booking_service
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.user import require_admin


router = APIRouter(tags=["bookings"])

@router.post("", response_model=BookingOut)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return booking_service.create_booking(db, current_user.id, booking_data)

# GET /bookings - user sees theirs; admin sees all
@router.get("", response_model=List[BookingOut])
def list_bookings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    status: Optional[str] = Query(None),
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
):
    is_admin = getattr(current_user, "is_admin", False)
    return booking_service.get_bookings(db, current_user, is_admin, status, start, end)


# GET /bookings/{id}
@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(
    booking_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    is_admin = getattr(current_user, "is_admin", False)
    return booking_service.get_booking(db, booking_id, current_user, is_admin)



# PATCH /bookings/{id}
@router.patch("/{booking_id}", response_model=BookingOut)
def update_booking(
    booking_id: uuid.UUID,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),  # ✅ only admins allowed
):
    return booking_service.update_booking(db, booking_id, booking_update, current_user)


# DELETE /bookings/{id}
@router.delete("/{booking_id}")
def delete_booking(
    booking_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    is_admin = getattr(current_user, "is_admin", False)
    return booking_service.delete_booking(db, booking_id, current_user, is_admin)