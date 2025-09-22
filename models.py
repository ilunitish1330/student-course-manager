from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


# -------------------
# Student Models
# -------------------
class StudentBase(SQLModel):
    name: str
    email: str
    roll_no: str


class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int
    created_at: datetime


# -------------------
# Course Models
# -------------------
class CourseBase(SQLModel):
    code: str
    title: str
    credits: int


class Course(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: int
    created_at: datetime


# -------------------
# Enrollment Models
# -------------------
class EnrollmentBase(SQLModel):
    student_id: int
    course_id: int
    grade: Optional[str] = None


class Enrollment(EnrollmentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    enrolled_on: datetime = Field(default_factory=datetime.utcnow)


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    id: int
    enrolled_on: datetime
