from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from typing import List

from app.schemas.review import ReviewOut, ReviewCreate, ReviewUpdate
from app.services import review as review_service
from app.core.database import get_db
from app.core.security import get_current_user
from app.services.user import require_admin

router = APIRouter()

@router.post("", response_model=ReviewOut)
def create_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return review_service.create_review(db, current_user.id, review_data)


@router.get("/services/{service_id}", response_model=List[ReviewOut])
def get_reviews_for_service(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    return review_service.get_reviews_for_service(db, service_id)

@router.patch("/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: uuid.UUID,
    review_data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return review_service.update_review(db, current_user.id, review_id, review_data)


@router.delete("/{review_id}")
def delete_review(
    review_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Check if admin
    is_admin = getattr(current_user, "is_admin", False)
    return review_service.delete_review(db, current_user.id, review_id, is_admin)