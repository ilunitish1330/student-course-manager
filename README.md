# 🎓 Student-Course Management System

A full-stack application for managing students, courses, and enrollments with **FastAPI backend** and **Streamlit frontend**.

---

## 🚀 Features
- Add, update, delete students
- Add, update, delete courses
- Enroll students into courses
- Manage grades for enrollments
- Dashboard with previous enrollments
- Simple login system

---

## 🛠️ Tech Stack
- **Backend**: FastAPI + SQLModel + SQLite
- **Frontend**: Streamlit
- **Language**: Python 3.12

---

## 📂 Project Structure
student-course-manager/
│── app/
│ ├── api/ # FastAPI routes
│ ├── crud/ # CRUD operations
│ ├── models.py # Database models
│ ├── db.py # DB connection
│── ui/
│ ├── main_ui.py # Streamlit app
│── school.db # SQLite database
│── README.md # Project description