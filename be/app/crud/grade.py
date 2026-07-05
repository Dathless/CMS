from sqlalchemy.orm import Session

from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeUpdate


def get_grade(db: Session, grade_id: int):
    return db.query(Grade).filter(Grade.id == grade_id).first()


def get_grades_by_enrollment(db: Session, enrollment_id: int):
    return db.query(Grade).filter(Grade.enrollment_id == enrollment_id).all()


def create_grade(db: Session, grade: GradeCreate):
    db_grade = Grade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


def update_grade(db: Session, grade_id: int, grade: GradeUpdate):
    db_grade = get_grade(db, grade_id)
    if not db_grade:
        return None
    update_data = grade.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_grade, key, value)
    db.commit()
    db.refresh(db_grade)
    return db_grade


def delete_grade(db: Session, grade_id: int):
    db_grade = get_grade(db, grade_id)
    if not db_grade:
        return False
    db.delete(db_grade)
    db.commit()
    return True
