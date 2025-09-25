import uuid
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from datetime import datetime


class Service(Base):
    __tablename__ = "services"


    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    bookings = relationship("Booking", back_populates="service", cascade=["all", "delete-orphan"])