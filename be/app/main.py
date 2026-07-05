from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.core.init_db import init_database
from app.routers import auth, users, courses, enrollments, grades

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(courses.router, prefix=settings.API_V1_STR)
app.include_router(enrollments.router, prefix=settings.API_V1_STR)
app.include_router(grades.router, prefix=settings.API_V1_STR)


@app.on_event("startup")
def on_startup():
    init_database()

@app.get("/")
def root():
    return {"message": "Course Management System API"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0",
        port=8000,
        reload=True,
    )