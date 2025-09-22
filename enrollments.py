from sqlmodel import Session, select
from app.models import Enrollment, EnrollmentCreate

def create_enrollment(session: Session, enrollment_in: EnrollmentCreate):
    enrollment = Enrollment.from_orm(enrollment_in)
    session.add(enrollment)
    session.commit()
    session.refresh(enrollment)
    return enrollment

def get_enrollments(session: Session, skip: int = 0, limit: int = 100):
    statement = select(Enrollment).offset(skip).limit(limit)
    return session.scalars(statement).all()

def get_enrollment(session: Session, enrollment_id: int):
    return session.get(Enrollment, enrollment_id)

def update_enrollment(session: Session, enrollment_id: int, enrollment_in: EnrollmentCreate):
    enrollment = session.get(Enrollment, enrollment_id)
    if not enrollment:
        return None
    enrollment.student_id = enrollment_in.student_id
    enrollment.course_id = enrollment_in.course_id
    enrollment.grade = enrollment_in.grade
    session.add(enrollment)
    session.commit()
    session.refresh(enrollment)
    return enrollment

def delete_enrollment(session: Session, enrollment_id: int):
    enrollment = session.get(Enrollment, enrollment_id)
    if not enrollment:
        return None
    session.delete(enrollment)
    session.commit()
    return True
