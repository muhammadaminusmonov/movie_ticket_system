import uuid

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)