from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import review as review_repo, booking as booking_repo
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
import uuid

def create_review(db: Session, user_id, review_data: ReviewCreate):
    booking = booking_repo.get_booking(db, review_data.booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your booking")

    if booking.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="You can only review completed bookings"
        )

    existing_review = review_repo.get_review_by_booking(db, booking.id)
    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="A review already exists for this booking"
        )

    review = Review(
        booking_id=booking.id,
        rating=review_data.rating,
        comment=review_data.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_review(db: Session, review_id: uuid.UUID):
    review = review_repo.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")
    return review


def get_reviews_for_service(db: Session, service_id: uuid.UUID):
    return review_repo.get_reviews_by_service(db, service_id)


def update_review(db: Session, user_id: uuid.UUID, review_id: uuid.UUID, review_data: ReviewUpdate):
    review = get_review(db, review_id)
    
    if review.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only update your own review.")

    return review_repo.update_review(db, review, review_data)


def delete_review(db: Session, user_id: uuid.UUID, review_id: uuid.UUID, is_admin: bool = False):
    review = get_review(db, review_id)
    
    if review.user_id != user_id and not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review.")

    review_repo.delete_review(db, review)
    return {"detail": "Review deleted successfully"}