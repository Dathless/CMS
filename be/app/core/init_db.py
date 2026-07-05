from app.core.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.grade import Grade
from app.models.refresh_token import RefreshToken
from app.core.security import get_password_hash


def init_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.username == "admin1").first()
        if not existing_admin:
            seed_data = [
                User(
                    username="admin1",
                    password_hash=get_password_hash("123456"),
                    email="admin1@example.com",
                    full_name="Admin One",
                    role="admin",
                ),
                User(
                    username="giangvien1",
                    password_hash=get_password_hash("123456"),
                    email="giangvien1@example.com",
                    full_name="Giảng Viên Một",
                    role="lecturer",
                ),
                User(
                    username="sinhvien1",
                    password_hash=get_password_hash("123456"),
                    email="sinhvien1@example.com",
                    full_name="Sinh Viên Một",
                    role="student",
                ),
            ]
            db.add_all(seed_data)
            db.commit()
            print("Database initialized with seed data.")
        else:
            print("Database already initialized.")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
