from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate


def get_enrollment(db: Session, enrollment_id: int):
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()


def get_enrollments(db: Session, skip: int = 0, limit: int = 100, course_id: int = None, student_id: int = None):
    query = db.query(Enrollment)
    if course_id:
        query = query.filter(Enrollment.course_id == course_id)
    if student_id:
        query = query.filter(Enrollment.student_id == student_id)
    return query.offset(skip).limit(limit).all()


def create_enrollment(db: Session, enrollment: EnrollmentCreate):
    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def update_enrollment(db: Session, enrollment_id: int, enrollment: EnrollmentUpdate):
    db_enrollment = get_enrollment(db, enrollment_id)
    if not db_enrollment:
        return None
    update_data = enrollment.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_enrollment, key, value)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def delete_enrollment(db: Session, enrollment_id: int):
    db_enrollment = get_enrollment(db, enrollment_id)
    if not db_enrollment:
        return False
    db.delete(db_enrollment)
    db.commit()
    return True
