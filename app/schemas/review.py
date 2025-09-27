from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Optional

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    booking_id: uuid.UUID = Field(
        ...,
        example="00000000-0000-0000-0000-000000000000"
    )

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class ReviewOut(ReviewBase):
    id: uuid.UUID
    booking_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True