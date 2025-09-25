import uuid

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.schemas.user import RoleEnum
from app.models.booking import Booking
from app.models.review import Review



class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)
    created_at = Column(DateTime, default=func.now())

    bookings = relationship("Booking", back_populates="user", cascade=["all", "delete-orphan"])
    reviews = relationship("Review", secondary="bookings", back_populates="user", overlaps="reviews,bookings")
