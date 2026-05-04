import uuid
from sqlalchemy import Column, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class BookingSeat(Base):
    __tablename__ = "booking_seats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False)
    seat_id = Column(UUID(as_uuid=True), ForeignKey("seats.id"), nullable=False)
    show_id = Column(UUID(as_uuid=True), ForeignKey("shows.id"), nullable=False)

    price = Column(Numeric(10, 2), nullable=False)

    # relationships
    booking = relationship("Booking", back_populates="seats")

    __table_args__ = (
        UniqueConstraint("seat_id", "show_id", name="uq_seat_show"),
    )