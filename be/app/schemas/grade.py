from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GradeBase(BaseModel):
    enrollment_id: int
    score: Optional[float] = None
    feedback: Optional[str] = None


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    score: Optional[float] = None
    feedback: Optional[str] = None


class GradeResponse(GradeBase):
    id: int
    graded_at: datetime

    model_config = {"from_attributes": True}
