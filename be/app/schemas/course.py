from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    lecturer_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None


class CourseResponse(CourseBase):
    id: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
