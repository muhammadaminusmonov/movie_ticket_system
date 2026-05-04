import uuid
import enum
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class CartStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CHECKED_OUT = "CHECKED_OUT"


class Cart(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(CartStatus), nullable=False, default=CartStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")