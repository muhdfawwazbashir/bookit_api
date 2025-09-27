from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate
from app.models.booking import Booking
from typing import List, Optional
import uuid

def create_review(db: Session, user_id: uuid.UUID, review_data: ReviewCreate) -> Review:
    review = Review(
        booking_id=review_data.booking_id,
        # user_id=user_id,
        rating=review_data.rating,
        comment=review_data.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_review(db: Session, review_id: uuid.UUID) -> Optional[Review]:
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews_by_service(db: Session, service_id: uuid.UUID): 
    return (
        db.query(Review)
        .join(Booking)
        .filter(Booking.service_id == service_id)
        .all()
    )

def update_review(db: Session, review: Review, review_data: ReviewUpdate) -> Review:
    for field, value in review_data.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    db.commit()
    db.refresh(review)
    return review

def delete_review(db: Session, review: Review) -> None:
    db.delete(review)
    db.commit()

def get_review_by_booking(db: Session, booking_id: uuid.UUID):
    return db.query(Review).filter(Review.booking_id == booking_id).first()