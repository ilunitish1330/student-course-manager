from sqlmodel import Session, select
from app.models import Student, StudentCreate

def create_student(session: Session, student_in: StudentCreate):
    student = Student.from_orm(student_in)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def get_students(session: Session, skip: int = 0, limit: int = 100):
    statement = select(Student).offset(skip).limit(limit)
    return session.scalars(statement).all()

def get_student(session: Session, student_id: int):
    return session.get(Student, student_id)

def update_student(session: Session, student_id: int, student_in: StudentCreate):
    student = session.get(Student, student_id)
    if not student:
        return None
    student.name = student_in.name
    student.email = student_in.email
    student.roll_no = student_in.roll_no
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def delete_student(session: Session, student_id: int):
    student = session.get(Student, student_id)
    if not student:
        return None
    session.delete(student)
    session.commit()
    return True
