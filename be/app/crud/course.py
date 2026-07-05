from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100, lecturer_id: int = None):
    query = db.query(Course)
    if lecturer_id:
        query = query.filter(Course.lecturer_id == lecturer_id)
    return query.offset(skip).limit(limit).all()


def create_course(db: Session, course: CourseCreate):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, course: CourseUpdate):
    db_course = get_course(db, course_id)
    if not db_course:
        return None
    update_data = course.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int):
    db_course = get_course(db, course_id)
    if not db_course:
        return False
    db.delete(db_course)
    db.commit()
    return True
