from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select

from app.database import DbSession
from app.dependencies import get_current_user
from app.models import Course, User
from app.schemas import CourseCreate, CourseRead, CourseUpdate

router = APIRouter(prefix="/courses", tags=["courses"])

CurrentUser = Annotated[User, Depends(get_current_user)]


def get_owned_course(db: DbSession, course_id: int, user: User) -> Course:
    """Fetch a course only if it belongs to `user`; otherwise 404."""
    stmt = select(Course).where(Course.id == course_id, Course.owner_id == user.id)
    course = db.scalar(stmt)
    if course is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Course not found")
    return course


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(data: CourseCreate, db: DbSession, user: CurrentUser):
    course = Course(**data.model_dump(), owner_id=user.id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("", response_model=list[CourseRead])
def list_courses(db: DbSession, user: CurrentUser):
    stmt = select(Course).where(Course.owner_id == user.id).order_by(Course.id)
    return db.scalars(stmt).all()


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: DbSession, user: CurrentUser):
    return get_owned_course(db, course_id, user)


@router.patch("/{course_id}", response_model=CourseRead)
def update_course(
    course_id: int, data: CourseUpdate, db: DbSession, user: CurrentUser
):
    course = get_owned_course(db, course_id, user)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: DbSession, user: CurrentUser):
    course = get_owned_course(db, course_id, user)
    db.delete(course)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)