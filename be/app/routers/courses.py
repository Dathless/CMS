from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.crud.course import get_course, get_courses, create_course, update_course, delete_course
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.models.user import User

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/", response_model=list[CourseResponse])
def read_courses(
    skip: int = 0,
    limit: int = 100,
    lecturer_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_courses(db, skip=skip, limit=limit, lecturer_id=lecturer_id)


@router.get("/{course_id}", response_model=CourseResponse)
def read_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_course = get_course(db, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_new_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "lecturer")),
):
    return create_course(db, course)


@router.put("/{course_id}", response_model=CourseResponse)
def update_existing_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ("admin", "lecturer"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    db_course = get_course(db, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role == "lecturer" and db_course.lecturer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated = update_course(db, course_id, course)
    if not updated:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated


@router.delete("/{course_id}")
def delete_existing_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    deleted = delete_course(db, course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}
