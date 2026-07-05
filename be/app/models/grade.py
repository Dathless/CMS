from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey

from app.core.database import Base


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    graded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
