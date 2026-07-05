from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.crud.grade import get_grade, get_grades_by_enrollment, create_grade, update_grade, delete_grade
from app.crud.enrollment import get_enrollment
from app.schemas.grade import GradeCreate, GradeUpdate, GradeResponse
from app.models.user import User

router = APIRouter(prefix="/grades", tags=["grades"])


@router.get("/enrollment/{enrollment_id}", response_model=list[GradeResponse])
def read_grades_by_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    enrollment = get_enrollment(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if current_user.role == "student" and enrollment.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if current_user.role == "lecturer":
        from app.models.course import Course
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        if not course or course.lecturer_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return get_grades_by_enrollment(db, enrollment_id)


@router.get("/{grade_id}", response_model=GradeResponse)
def read_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_grade = get_grade(db, grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    enrollment = get_enrollment(db, db_grade.enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if current_user.role == "student" and enrollment.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if current_user.role == "lecturer":
        from app.models.course import Course
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        if not course or course.lecturer_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return db_grade


@router.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
def create_new_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ("admin", "lecturer"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    enrollment = get_enrollment(db, grade.enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if current_user.role == "lecturer":
        from app.models.course import Course
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        if not course or course.lecturer_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return create_grade(db, grade)


@router.put("/{grade_id}", response_model=GradeResponse)
def update_existing_grade(
    grade_id: int,
    grade: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ("admin", "lecturer"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_grade = get_grade(db, grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    enrollment = get_enrollment(db, db_grade.enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if current_user.role == "lecturer":
        from app.models.course import Course
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()
        if not course or course.lecturer_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    updated = update_grade(db, grade_id, grade)
    if not updated:
        raise HTTPException(status_code=404, detail="Grade not found")
    return updated


@router.delete("/{grade_id}")
def delete_existing_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ("admin",):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_grade = get_grade(db, grade_id)
    if not db_grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    deleted = delete_grade(db, grade_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Grade not found")
    return {"message": "Grade deleted successfully"}
