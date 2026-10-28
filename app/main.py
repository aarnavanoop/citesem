from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title= "StudyPilot API")

class CourseCreate(BaseModel):
    name: str
    description: str | None = None
    unit_code: str


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status" : "healthy"}

@app.get("/version", status_code=status.HTTP_200_OK)
def get_version():
    return{
        "version": "0.1.0",
        "environment": "development"
    }

@app.post("/courses", status_code = status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    return {"message": "Course Created", "data":course}
