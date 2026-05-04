import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Screen(Base):
    __tablename__ = "screens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    cinema_id = Column(UUID(as_uuid=True), ForeignKey("cinemas.id"), nullable=False)