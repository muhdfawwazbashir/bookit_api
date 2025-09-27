import uuid
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from app.core.database import Base
from datetime import datetime
from app.models.booking import Booking

class Review(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), ForeignKey('bookings.id'))
    rating = Column(Integer)  # 1 to 5
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    booking = relationship("Booking", back_populates="reviews", foreign_keys=[booking_id])
    

    @hybrid_property
    def user_id(self):
        return self.booking.user_id   # ✅ comes from Booking

    @hybrid_property
    def service_id(self):
        return self.booking.service_id 