from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None


class EnrollmentResponse(EnrollmentBase):
    id: int
    status: str
    enrolled_at: datetime

    model_config = {"from_attributes": True}
