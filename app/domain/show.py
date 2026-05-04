import uuid

from sqlalchemy import Column, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Show(Base):
    __tablename__ = "shows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id"), nullable=False)
    screen_id = Column(UUID(as_uuid=True), ForeignKey("screens.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)