from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid
from enum import Enum


class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class BookingBase(BaseModel):
    service_id: uuid.UUID = Field(
        ...,
        example="00000000-0000-0000-0000-000000000000"
    )
    start_time: datetime
    end_time: datetime


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[BookingStatus] = None


class BookingOut(BookingBase):
    id: uuid.UUID
    user_id: uuid.UUID
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True