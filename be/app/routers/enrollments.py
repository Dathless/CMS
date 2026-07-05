from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.crud.enrollment import (
    get_enrollment,
    get_enrollments,
    create_enrollment,
    update_enrollment,
    delete_enrollment,
)
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse
from app.models.user import User

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.get("/", response_model=list[EnrollmentResponse])
def read_enrollments(
    skip: int = 0,
    limit: int = 100,
    course_id: int = None,
    student_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "student":
        student_id = current_user.id
    return get_enrollments(db, skip=skip, limit=limit, course_id=course_id, student_id=student_id)


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def read_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_enrollment = get_enrollment(db, enrollment_id)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return db_enrollment


@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_new_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "student":
        if enrollment.student_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return create_enrollment(db, enrollment)


@router.put("/{enrollment_id}", response_model=EnrollmentResponse)
def update_existing_enrollment(
    enrollment_id: int,
    enrollment: EnrollmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "lecturer")),
):
    updated = update_enrollment(db, enrollment_id, enrollment)
    if not updated:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return updated


@router.delete("/{enrollment_id}")
def delete_existing_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    deleted = delete_enrollment(db, enrollment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return {"message": "Enrollment deleted successfully"}
