import uuid
import enum

from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class SeatType(str, enum.Enum):
    STANDARD = "STANDARD"
    VIP = "VIP"


class Seat(Base):
    __tablename__ = "seats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    screen_id = Column(UUID(as_uuid=True), ForeignKey("screens.id"), nullable=False)
    row = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    type = Column(Enum(SeatType), nullable=False, default=SeatType.STANDARD)