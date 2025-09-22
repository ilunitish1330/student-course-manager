from sqlmodel import Session, select
from app.models import Course, CourseCreate

def create_course(session: Session, course_in: CourseCreate):
    course = Course.from_orm(course_in)
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

def get_courses(session: Session, skip: int = 0, limit: int = 100):
    statement = select(Course).offset(skip).limit(limit)
    return session.scalars(statement).all()

def get_course(session: Session, course_id: int):
    return session.get(Course, course_id)

def update_course(session: Session, course_id: int, course_in: CourseCreate):
    course = session.get(Course, course_id)
    if not course:
        return None
    course.code = course_in.code
    course.title = course_in.title
    course.credits = course_in.credits
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

def delete_course(session: Session, course_id: int):
    course = session.get(Course, course_id)
    if not course:
        return None
    session.delete(course)
    session.commit()
    return True
