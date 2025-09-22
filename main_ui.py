# # import streamlit as st
# # import httpx

# # # ------------------------
# # # Configure API base here
# # # ------------------------
# # API_BASE = "http://192.168.11.104:8001/api"  # update if different

# # # ------------------------
# # # Dummy login credentials
# # # ------------------------
# # USER_CREDENTIALS = {
# #     "admin": "admin123"
# # }

# # # ------------------------
# # # HTTP helpers (safe)
# # # ------------------------
# # def safe_get(path: str):
# #     url = f"{API_BASE}{path}/?skip=0&limit=100"
# #     try:
# #         with httpx.Client(timeout=6.0) as client:
# #             r = client.get(url)
# #             if r.status_code == 200:
# #                 return r.json() if r.text.strip() else []
# #             else:
# #                 st.error(f"GET {path} failed: {r.status_code} {r.text}")
# #                 return []
# #     except Exception as e:
# #         st.error(f"GET {path} failed: {e}")
# #         return []


# # def safe_post(path: str, data: dict):
# #     url = f"{API_BASE}{path}"
# #     headers = {"accept": "application/json", "Content-Type": "application/json"}
# #     try:
# #         with httpx.Client(timeout=6.0) as client:
# #             return client.post(url=url, headers=headers, json=data)
# #     except Exception as e:
# #         st.error(f"POST {path} failed: {e}")
# #         return None


# # def safe_delete(path: str):
# #     url = f"{API_BASE}{path}"
# #     try:
# #         with httpx.Client(timeout=6.0) as client:
# #             return client.delete(url)
# #     except Exception as e:
# #         st.error(f"DELETE {path} failed: {e}")
# #         return None


# # def safe_put(path: str, data: dict = None):
# #     url = f"{API_BASE}{path}"
# #     try:
# #         with httpx.Client(timeout=6.0) as client:
# #             return client.put(url, json=data)
# #     except Exception as e:
# #         st.error(f"PUT {path} failed: {e}")
# #         return None


# # # ------------------------
# # # Dashboard
# # # ------------------------
# # def show_dashboard():
# #     st.title("📊 Student-Course Manager — Dashboard")

# #     students = safe_get("/students")
# #     courses = safe_get("/courses")
# #     enrollments = safe_get("/enrollments")

# #     col1, col2, col3 = st.columns(3)
# #     col1.metric("Students", len(students))
# #     col2.metric("Courses", len(courses))
# #     col3.metric("Enrollments", len(enrollments))

# #     st.markdown("---")
# #     st.subheader("Recent enrollments (latest 5)")
# #     if enrollments:
# #         student_map = {s["id"]: s.get("name", str(s["id"])) for s in students}
# #         course_map = {c["id"]: c.get("title", c.get("code", str(c["id"]))) for c in courses}
# #         for e in enrollments[-5:][::-1]:
# #             sid, cid = e.get("student_id"), e.get("course_id")
# #             grade = e.get("grade") or "N/A"
# #             st.write(f"- #{e.get('id')} — **{student_map.get(sid, sid)}** → **{course_map.get(cid, cid)}** (grade: {grade})")
# #     else:
# #         st.info("No enrollments yet.")


# # # ------------------------
# # # Students
# # # ------------------------
# # def manage_students():
# #     st.title("👩‍🎓 Manage Students")

# #     st.subheader("➕ Add student")
# #     with st.form("add_student", clear_on_submit=True):
# #         name = st.text_input("Name")
# #         email = st.text_input("Email")
# #         roll_no = st.text_input("Roll No")
# #         if st.form_submit_button("Create"):
# #             payload = {"name": name, "email": email, "roll_no": roll_no}
# #             resp = safe_post("/students/post", payload)
# #             if resp and resp.status_code in (200, 201):
# #                 st.success("Student added")
# #                 st.rerun()

# #     st.subheader("📋 Students list")
# #     students = safe_get("/students")
# #     if not students:
# #         st.info("No students to show.")
# #         return

# #     for s in students:
# #         with st.expander(f"ID {s['id']} — {s['name']}"):
# #             st.write(f"Roll No: {s['roll_no']} | Email: {s['email']}")

# #             # Update form
# #             with st.form(f"update_student_{s['id']}", clear_on_submit=True):
# #                 new_name = st.text_input("Edit name", value=s["name"])
# #                 new_email = st.text_input("Edit email", value=s["email"])
# #                 new_roll = st.text_input("Edit roll no", value=s["roll_no"])
# #                 if st.form_submit_button("Update"):
# #                     data = {"name": new_name, "email": new_email, "roll_no": new_roll}
# #                     r = safe_put(f"/students/update/?student_id={s['id']}", data)
# #                     if r and r.status_code == 200:
# #                         st.success("Student updated")
# #                         st.rerun()

# #             # Delete button
# #             if st.button("❌ Delete", key=f"del_student_{s['id']}"):
# #                 r = safe_delete(f"/students/delete/?student_id={s['id']}")
# #                 if r and r.status_code in (200, 204):
# #                     st.warning("Student deleted")
# #                     st.rerun()


# # # ------------------------
# # # Courses
# # # ------------------------
# # def manage_courses():
# #     st.title("📘 Manage Courses")

# #     st.subheader("➕ Add course")
# #     with st.form("add_course", clear_on_submit=True):
# #         code = st.text_input("Course code")
# #         title = st.text_input("Title")
# #         credits = st.number_input("Credits", min_value=0, step=1)
# #         if st.form_submit_button("Create"):
# #             payload = {"code": code, "title": title, "credits": int(credits)}
# #             resp = safe_post("/courses/post", payload)
# #             if resp and resp.status_code in (200, 201):
# #                 st.success("Course added")
# #                 st.rerun()

# #     st.subheader("📋 Courses list")
# #     courses = safe_get("/courses")
# #     if not courses:
# #         st.info("No courses found.")
# #         return

# #     for c in courses:
# #         with st.expander(f"ID {c['id']} — {c['title']}"):
# #             st.write(f"Code: {c['code']} | Credits: {c['credits']}")

# #             # Update form
# #             with st.form(f"update_course_{c['id']}", clear_on_submit=True):
# #                 new_code = st.text_input("Edit code", value=c["code"])
# #                 new_title = st.text_input("Edit title", value=c["title"])
# #                 new_credits = st.number_input("Edit credits", value=c["credits"], step=1)
# #                 if st.form_submit_button("Update"):
# #                     data = {"code": new_code, "title": new_title, "credits": int(new_credits)}
# #                     r = safe_put(f"/courses/update/?course_id={c['id']}", data)
# #                     if r and r.status_code == 200:
# #                         st.success("Course updated")
# #                         st.rerun()

# #             # Delete button
# #             if st.button("❌ Delete", key=f"del_course_{c['id']}"):
# #                 r = safe_delete(f"/courses/delete/?course_id={c['id']}")
# #                 if r and r.status_code in (200, 204):
# #                     st.warning("Course deleted")
# #                     st.rerun()


# # # ------------------------
# # # Enrollments
# # # ------------------------
# # def manage_enrollments():
# #     st.title("🎓 Manage Enrollments")

# #     students = safe_get("/students")
# #     courses = safe_get("/courses")

# #     student_options = {str(s["id"]): f"{s['id']} - {s['name']}" for s in students}
# #     course_options = {str(c["id"]): f"{c['id']} - {c['title']}" for c in courses}

# #     st.subheader("➕ Enroll a student")
# #     with st.form("add_enrollment", clear_on_submit=True):
# #         sid = st.selectbox("Student", options=list(student_options.keys()), format_func=lambda x: student_options[x])
# #         cid = st.selectbox("Course", options=list(course_options.keys()), format_func=lambda x: course_options[x])
# #         grade = st.text_input("Grade (optional)")
# #         if st.form_submit_button("Enroll"):
# #             payload = {"student_id": int(sid), "course_id": int(cid)}
# #             if grade:
# #                 payload["grade"] = grade
# #             resp = safe_post("/enrollments/post", payload)
# #             if resp and resp.status_code in (200, 201):
# #                 st.success("Enrolled")
# #                 st.rerun()

# #     st.subheader("📋 Enrollments list")
# #     enrollments = safe_get("/enrollments")
# #     if not enrollments:
# #         st.info("No enrollments yet.")
# #         return

# #     student_map = {s["id"]: s["name"] for s in students}
# #     course_map = {c["id"]: c["title"] for c in courses}

# #     for e in enrollments:
# #         with st.expander(f"Enroll #{e['id']}"):
# #             sid, cid = e.get("student_id"), e.get("course_id")
# #             st.write(f"Student: {student_map.get(sid, sid)} → Course: {course_map.get(cid, cid)}")

# #             # Update grade
# #             with st.form(f"update_enr_{e['id']}", clear_on_submit=True):
# #                 new_grade = st.text_input("Grade", value=e.get("grade") or "")
# #                 if st.form_submit_button("Update Grade"):
# #                     data = {"student_id": sid, "course_id": cid, "grade": new_grade}
# #                     r = safe_put(f"/enrollments/update/?enrollment_id={e['id']}", data)
# #                     if r and r.status_code == 200:
# #                         st.success("Enrollment updated")
# #                         st.rerun()

# #             # Delete
# #             if st.button("❌ Delete", key=f"del_enr_{e['id']}"):
# #                 r = safe_delete(f"/enrollments/delete/?enrollment_id={e['id']}")
# #                 if r and r.status_code in (200, 204):
# #                     st.warning("Enrollment deleted")
# #                     st.rerun()


# # # ------------------------
# # # Login Page
# # # ------------------------
# # def login_page():
# #     st.markdown(
# #         """
# #         <h1 style="text-align:center;">🎓 Student-Course Manager</h1>
# #         <p style="text-align:center; font-size:16px; color:gray;">
# #             Please log in to access the dashboard and manage students, courses, and enrollments.
# #         </p>
# #         """,
# #         unsafe_allow_html=True
# #     )

# #     # Create a centered form card
# #     with st.container():
# #         st.markdown(
# #             """
# #             <div style="padding:20px; border-radius:10px; background-color:#1e1e1e; text-align:center;">
# #             """,
# #             unsafe_allow_html=True,
# #         )

# #         username = st.text_input("👤 Username")
# #         password = st.text_input("🔑 Password", type="password")

# #         if st.button("Login"):
# #             if USER_CREDENTIALS.get(username) == password:
# #                 st.session_state.logged_in = True
# #                 st.session_state.username = username
# #                 st.success("✅ Login successful!")
# #                 st.rerun()
# #             else:
# #                 st.error("❌ Invalid username or password")

# #         st.markdown("</div>", unsafe_allow_html=True)



# # # ------------------------
# # # Main
# # # ------------------------
# # def main():
# #     if "logged_in" not in st.session_state:
# #         st.session_state.logged_in = False

# #     if not st.session_state.logged_in:
# #         login_page()
# #     else:
# #         st.sidebar.title("Navigation")
# #         st.sidebar.write(f"👋 Logged in as: **{st.session_state.username}**")

# #         # Logout button
# #         if st.sidebar.button("Logout"):
# #             st.session_state.logged_in = False
# #             st.session_state.username = ""
# #             st.rerun()

# #         page = st.sidebar.radio("Go to", ["Dashboard", "Students", "Courses", "Enrollments"])

# #         if page == "Dashboard":
# #             show_dashboard()
# #         elif page == "Students":
# #             manage_students()
# #         elif page == "Courses":
# #             manage_courses()
# #         elif page == "Enrollments":
# #             manage_enrollments()
# #             if __name__ == "__main__":    
# #                 main()

# import streamlit as st
# import httpx

# # ------------------------
# # Configure API base here
# # ------------------------
# API_BASE = "http://192.168.11.104:8081/api"  # update if different

# # ------------------------
# # Dummy login credentials
# # ------------------------
# USER_CREDENTIALS = {
#     "admin": "admin123"
# }

# # ------------------------
# # HTTP helpers (safe)
# # ------------------------
# def safe_get(path: str):
#     url = f"{API_BASE}{path}/?skip=0&limit=100"
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             r = client.get(url)
#             if r.status_code == 200:
#                 return r.json() if r.text.strip() else []
#             else:
#                 st.error(f"GET {path} failed: {r.status_code} {r.text}")
#                 return []
#     except Exception as e:
#         st.error(f"GET {path} failed: {e}")
#         return []


# def safe_post(path: str, data: dict):
#     url = f"{API_BASE}{path}"
#     headers = {"accept": "application/json", "Content-Type": "application/json"}
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             return client.post(url=url, headers=headers, json=data)
#     except Exception as e:
#         st.error(f"POST {path} failed: {e}")
#         return None


# def safe_delete(path: str):
#     url = f"{API_BASE}{path}"
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             return client.delete(url)
#     except Exception as e:
#         st.error(f"DELETE {path} failed: {e}")
#         return None


# def safe_put(path: str, data: dict = None):
#     url = f"{API_BASE}{path}"
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             return client.put(url, json=data)
#     except Exception as e:
#         st.error(f"PUT {path} failed: {e}")
#         return None


# # ------------------------
# # Dashboard
# # ------------------------
# def show_dashboard():
#     st.title("📊 Student-Course Manager — Dashboard")

#     students = safe_get("/students")
#     courses = safe_get("/courses")
#     enrollments = safe_get("/enrollments")

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Students", len(students))
#     col2.metric("Courses", len(courses))
#     col3.metric("Enrollments", len(enrollments))

#     st.markdown("---")
#     st.subheader("Recent enrollments (latest 5)")
#     if enrollments:
#         student_map = {s["id"]: s.get("name", str(s["id"])) for s in students}
#         course_map = {c["id"]: c.get("title", c.get("code", str(c["id"]))) for c in courses}
#         for e in enrollments[-5:][::-1]:
#             sid, cid = e.get("student_id"), e.get("course_id")
#             grade = e.get("grade") or "N/A"
#             st.write(f"- #{e.get('id')} — **{student_map.get(sid, sid)}** → **{course_map.get(cid, cid)}** (grade: {grade})")
#     else:
#         st.info("No enrollments yet.")


# # ------------------------
# # Students
# # ------------------------
# def manage_students():
#     st.title("👩‍🎓 Manage Students")

#     st.subheader("➕ Add student")
#     with st.form("add_student", clear_on_submit=True):
#         name = st.text_input("Name")
#         email = st.text_input("Email")
#         roll_no = st.text_input("Roll No")
#         if st.form_submit_button("Create"):
#             payload = {"name": name, "email": email, "roll_no": roll_no}
#             resp = safe_post("/students/post", payload)
#             if resp and resp.status_code in (200, 201):
#                 st.success("Student added")
#                 st.rerun()

#     st.subheader("📋 Students list")
#     students = safe_get("/students")
#     if not students:
#         st.info("No students to show.")
#         return

#     # 🔍 Search
#     query = st.text_input("Search students by name, roll no, or email")
#     if query:
#         q = query.lower()
#         students = [
#             s for s in students
#             if q in s["name"].lower() or q in s["roll_no"].lower() or q in s["email"].lower()
#         ]

#     for s in students:
#         with st.expander(f"ID {s['id']} — {s['name']}"):
#             st.write(f"Roll No: {s['roll_no']} | Email: {s['email']}")

#             with st.form(f"update_student_{s['id']}", clear_on_submit=True):
#                 new_name = st.text_input("Edit name", value=s["name"])
#                 new_email = st.text_input("Edit email", value=s["email"])
#                 new_roll = st.text_input("Edit roll no", value=s["roll_no"])
#                 if st.form_submit_button("Update"):
#                     data = {"name": new_name, "email": new_email, "roll_no": new_roll}
#                     r = safe_put(f"/students/update/?student_id={s['id']}", data)
#                     if r and r.status_code == 200:
#                         st.success("Student updated")
#                         st.rerun()

#             if st.button("❌ Delete", key=f"del_student_{s['id']}"):
#                 r = safe_delete(f"/students/delete/?student_id={s['id']}")
#                 if r and r.status_code in (200, 204):
#                     st.warning("Student deleted")
#                     st.rerun()


# # ------------------------
# # Courses
# # ------------------------
# def manage_courses():
#     st.title("📘 Manage Courses")

#     st.subheader("➕ Add course")
#     with st.form("add_course", clear_on_submit=True):
#         code = st.text_input("Course code")
#         title = st.text_input("Title")
#         credits = st.number_input("Credits", min_value=0, step=1)
#         if st.form_submit_button("Create"):
#             payload = {"code": code, "title": title, "credits": int(credits)}
#             resp = safe_post("/courses/post", payload)
#             if resp and resp.status_code in (200, 201):
#                 st.success("Course added")
#                 st.rerun()

#     st.subheader("📋 Courses list")
#     courses = safe_get("/courses")
#     if not courses:
#         st.info("No courses found.")
#         return

#     # 🔍 Search
#     query = st.text_input("Search courses by code or title")
#     if query:
#         q = query.lower()
#         courses = [c for c in courses if q in c["code"].lower() or q in c["title"].lower()]

#     for c in courses:
#         with st.expander(f"ID {c['id']} — {c['title']}"):
#             st.write(f"Code: {c['code']} | Credits: {c['credits']}")

#             with st.form(f"update_course_{c['id']}", clear_on_submit=True):
#                 new_code = st.text_input("Edit code", value=c["code"])
#                 new_title = st.text_input("Edit title", value=c["title"])
#                 new_credits = st.number_input("Edit credits", value=c["credits"], step=1)
#                 if st.form_submit_button("Update"):
#                     data = {"code": new_code, "title": new_title, "credits": int(new_credits)}
#                     r = safe_put(f"/courses/update/?course_id={c['id']}", data)
#                     if r and r.status_code == 200:
#                         st.success("Course updated")
#                         st.rerun()

#             if st.button("❌ Delete", key=f"del_course_{c['id']}"):
#                 r = safe_delete(f"/courses/delete/?course_id={c['id']}")
#                 if r and r.status_code in (200, 204):
#                     st.warning("Course deleted")
#                     st.rerun()


# # ------------------------
# # Enrollments
# # ------------------------
# def manage_enrollments():
#     st.title("🎓 Manage Enrollments")

#     students = safe_get("/students")
#     courses = safe_get("/courses")
#     enrollments = safe_get("/enrollments")

#     student_map = {s["id"]: s["name"] for s in students}
#     course_map = {c["id"]: c["title"] for c in courses}

#     st.subheader("📋 Enrollments list")

#     # 🔍 Search
#     query = st.text_input("Search enrollments by student or course")
#     if query:
#         q = query.lower()
#         enrollments = [
#             e for e in enrollments
#             if q in student_map.get(e["student_id"], "").lower()
#             or q in course_map.get(e["course_id"], "").lower()
#         ]

#     if not enrollments:
#         st.info("No enrollments found.")
#         return

#     for e in enrollments:
#         with st.expander(f"Enroll #{e['id']}"):
#             sid, cid = e.get("student_id"), e.get("course_id")
#             st.write(f"Student: {student_map.get(sid, sid)} → Course: {course_map.get(cid, cid)} | Grade: {e.get('grade','N/A')}")

#             with st.form(f"update_enr_{e['id']}", clear_on_submit=True):
#                 new_grade = st.text_input("Grade", value=e.get("grade") or "")
#                 if st.form_submit_button("Update Grade"):
#                     data = {"student_id": sid, "course_id": cid, "grade": new_grade}
#                     r = safe_put(f"/enrollments/update/?enrollment_id={e['id']}", data)
#                     if r and r.status_code == 200:
#                         st.success("Enrollment updated")
#                         st.rerun()

#             if st.button("❌ Delete", key=f"del_enr_{e['id']}"):
#                 r = safe_delete(f"/enrollments/delete/?enrollment_id={e['id']}")
#                 if r and r.status_code in (200, 204):
#                     st.warning("Enrollment deleted")
#                     st.rerun()


# # ------------------------
# # Login Page
# # ------------------------
# def login_page():
#     st.markdown(
#         """
#         <h1 style="text-align:center;">🎓 Student-Course Manager</h1>
#         <p style="text-align:center; font-size:16px; color:gray;">
#             Please log in to access the dashboard and manage students, courses, and enrollments.
#         </p>
#         """,
#         unsafe_allow_html=True
#     )

#     username = st.text_input("👤 Username")
#     password = st.text_input("🔑 Password", type="password")

#     if st.button("Login"):
#         if USER_CREDENTIALS.get(username) == password:
#             st.session_state.logged_in = True
#             st.session_state.username = username
#             st.success("✅ Login successful!")
#             st.rerun()
#         else:
#             st.error("❌ Invalid username or password")


# # ------------------------
# # Main
# # ------------------------
# def main():
#     if "logged_in" not in st.session_state:
#         st.session_state.logged_in = False

#     if not st.session_state.logged_in:
#         login_page()
#     else:
#         st.sidebar.title("Navigation")
#         st.sidebar.write(f"👋 Logged in as: **{st.session_state.username}**")

#         if st.sidebar.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.username = ""
#             st.rerun()

#         page = st.sidebar.radio("Go to", ["Dashboard", "Students", "Courses", "Enrollments"])

#         if page == "Dashboard":
#             show_dashboard()
#         elif page == "Students":
#             manage_students()
#         elif page == "Courses":
#             manage_courses()
#         elif page == "Enrollments":
#             manage_enrollments()


# if __name__ == "__main__":
#     main()

# import streamlit as st
# import httpx

# # ------------------------
# # Configure API base here
# # ------------------------
# API_BASE = "http://192.168.11.104:8081/api"  # update if different

# # ------------------------
# # Dummy login credentials (with roles)
# # ------------------------
# USER_CREDENTIALS = {
#     "admin": {"password": "admin123", "role": "admin"},
#     "viewer": {"password": "viewer123", "role": "viewer"},
# }

# # ------------------------
# # HTTP helpers (safe)
# # ------------------------
# def safe_get(path: str):
#     url = f"{API_BASE}{path}/?skip=0&limit=100"
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             r = client.get(url)
#             if r.status_code == 200:
#                 return r.json() if r.text.strip() else []
#             else:
#                 st.error(f"GET {path} failed: {r.status_code} {r.text}")
#                 return []
#     except Exception as e:
#         st.error(f"GET {path} failed: {e}")
#         return []


# def safe_post(path: str, data: dict):
#     url = f"{API_BASE}{path}"
#     headers = {"accept": "application/json", "Content-Type": "application/json"}
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             return client.post(url=url, headers=headers, json=data)
#     except Exception as e:
#         st.error(f"POST {path} failed: {e}")
#         return None


# def safe_delete(path: str):
#     url = f"{API_BASE}{path}"
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             return client.delete(url)
#     except Exception as e:
#         st.error(f"DELETE {path} failed: {e}")
#         return None


# def safe_put(path: str, data: dict = None):
#     url = f"{API_BASE}{path}"
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             return client.put(url, json=data)
#     except Exception as e:
#         st.error(f"PUT {path} failed: {e}")
#         return None


# # ------------------------
# # Dashboard
# # ------------------------
# def show_dashboard():
#     st.title("📊 Student-Course Manager — Dashboard")

#     students = safe_get("/students")
#     courses = safe_get("/courses")
#     enrollments = safe_get("/enrollments")

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Students", len(students))
#     col2.metric("Courses", len(courses))
#     col3.metric("Enrollments", len(enrollments))

#     st.markdown("---")
#     st.subheader("Recent enrollments (latest 5)")
#     if enrollments:
#         student_map = {s["id"]: s.get("name", str(s["id"])) for s in students}
#         course_map = {c["id"]: c.get("title", c.get("code", str(c["id"]))) for c in courses}
#         for e in enrollments[-5:][::-1]:
#             sid, cid = e.get("student_id"), e.get("course_id")
#             grade = e.get("grade") or "N/A"
#             st.write(
#                 f"- #{e.get('id')} — **{student_map.get(sid, sid)}** → **{course_map.get(cid, cid)}** (grade: {grade})"
#             )
#     else:
#         st.info("No enrollments yet.")


# # ------------------------
# # Students
# # ------------------------
# def manage_students():
#     st.title("👩‍🎓 Manage Students")

#     # ------------------------
#     # Admin-only add form
#     # ------------------------
#     if st.session_state.username == "admin":
#         st.subheader("➕ Add student")
#         with st.form("add_student", clear_on_submit=True):
#             name = st.text_input("Name")
#             email = st.text_input("Email")
#             roll_no = st.text_input("Roll No")
#             if st.form_submit_button("Create"):
#                 payload = {"name": name, "email": email, "roll_no": roll_no}
#                 resp = safe_post("/students/post", payload)
#                 if resp and resp.status_code in (200, 201):
#                     st.success("Student added")
#                     st.rerun()

#     st.subheader("📋 Students list")
#     students = safe_get("/students")
#     if not students:
#         st.info("No students to show.")
#         return

#     # 🔍 Search
#     query = st.text_input("Search students by name, roll no, or email", key="search_students")
#     if query:
#         q = query.lower()
#         students = [
#             s for s in students
#             if q in s["name"].lower() or q in s["roll_no"].lower() or q in s["email"].lower()
#         ]

#     for s in students:
#         with st.expander(f"ID {s['id']} — {s['name']}"):
#             st.write(f"Roll No: {s['roll_no']} | Email: {s['email']}")

#             # Admin-only update/delete
#             if st.session_state.username == "admin":
#                 with st.form(f"update_student_{s['id']}", clear_on_submit=True):
#                     new_name = st.text_input("Edit name", value=s["name"], key=f"name_{s['id']}")
#                     new_email = st.text_input("Edit email", value=s["email"], key=f"email_{s['id']}")
#                     new_roll = st.text_input("Edit roll no", value=s["roll_no"], key=f"roll_{s['id']}")
#                     if st.form_submit_button("Update"):
#                         data = {"name": new_name, "email": new_email, "roll_no": new_roll}
#                         r = safe_put(f"/students/update/?student_id={s['id']}", data)
#                         if r and r.status_code == 200:
#                             st.success("Student updated")
#                             st.rerun()

#                 if st.button("❌ Delete", key=f"del_student_{s['id']}"):
#                     r = safe_delete(f"/students/delete/?student_id={s['id']}")
#                     if r and r.status_code in (200, 204):
#                         st.warning("Student deleted")
#                         st.rerun()




# # ------------------------
# # Courses
# # ------------------------
# def manage_courses():
#     st.title("📘 Manage Courses")

#     # ------------------------
#     # Admin-only add form
#     # ------------------------
#     if st.session_state.username == "admin":
#         st.subheader("➕ Add course")
#         with st.form("add_course", clear_on_submit=True):
#             code = st.text_input("Course code")
#             title = st.text_input("Title")
#             credits = st.number_input("Credits", min_value=0, step=1)
#             if st.form_submit_button("Create"):
#                 payload = {"code": code, "title": title, "credits": int(credits)}
#                 resp = safe_post("/courses/post", payload)
#                 if resp and resp.status_code in (200, 201):
#                     st.success("Course added")
#                     st.rerun()

#     st.subheader("📋 Courses list")
#     courses = safe_get("/courses")
#     if not courses:
#         st.info("No courses found.")
#         return

#     # 🔍 Search
#     query = st.text_input("Search courses by code or title", key="search_courses")
#     if query:
#         q = query.lower()
#         courses = [c for c in courses if q in c["code"].lower() or q in c["title"].lower()]

#     for c in courses:
#         with st.expander(f"ID {c['id']} — {c['title']}"):
#             st.write(f"Code: {c['code']} | Credits: {c['credits']}")

#             # Admin-only update/delete
#             if st.session_state.username == "admin":
#                 with st.form(f"update_course_{c['id']}", clear_on_submit=True):
#                     new_code = st.text_input("Edit code", value=c["code"], key=f"code_{c['id']}")
#                     new_title = st.text_input("Edit title", value=c["title"], key=f"title_{c['id']}")
#                     new_credits = st.number_input("Edit credits", value=c["credits"], step=1, key=f"credits_{c['id']}")
#                     if st.form_submit_button("Update"):
#                         data = {"code": new_code, "title": new_title, "credits": int(new_credits)}
#                         r = safe_put(f"/courses/update/?course_id={c['id']}", data)
#                         if r and r.status_code == 200:
#                             st.success("Course updated")
#                             st.rerun()

#                 if st.button("❌ Delete", key=f"del_course_{c['id']}"):
#                     r = safe_delete(f"/courses/delete/?course_id={c['id']}")
#                     if r and r.status_code in (200, 204):
#                         st.warning("Course deleted")
#                         st.rerun()




# # ------------------------
# # Enrollments
# # ------------------------
# def manage_enrollments():
#     st.title("🎓 Manage Enrollments")

#     students = safe_get("/students")
#     courses = safe_get("/courses")
#     enrollments = safe_get("/enrollments")

#     student_map = {s["id"]: s["name"] for s in students}
#     course_map = {c["id"]: c["title"] for c in courses}

#     # ------------------------
#     # Only Admin can add/edit/delete
#     # ------------------------
#     if st.session_state.username == "admin":
#         st.subheader("➕ Enroll a student")
#         with st.form("add_enrollment", clear_on_submit=True):
#             sid = st.selectbox(
#                 "Student",
#                 options=[s["id"] for s in students],
#                 format_func=lambda x: student_map.get(x, x),
#                 key="single_enroll"
#             )
#             cid = st.selectbox(
#                 "Course",
#                 options=[c["id"] for c in courses],
#                 format_func=lambda x: course_map.get(x, x),
#                 key="single_course"
#             )
#             grade = st.text_input("Grade (optional)", key="single_grade")
#             if st.form_submit_button("Enroll"):
#                 payload = {"student_id": int(sid), "course_id": int(cid)}
#                 if grade:
#                     payload["grade"] = grade
#                 resp = safe_post("/enrollments/post", payload)
#                 if resp and resp.status_code in (200, 201):
#                     st.success("✅ Enrolled")
#                     st.rerun()

#         # Bulk enrollment by ID range
#         st.subheader("📤 Bulk Enroll Students by ID Range")
#         student_range = st.text_input("Enter Student ID Range (e.g., 1-10)", key="bulk_range")
#         course_input = st.text_input("Enter Course ID or Code", key="bulk_course")
#         grade_input = st.text_input("Grade (optional)", key="bulk_grade")

#         if st.button("Bulk Enroll"):
#             try:
#                 if "-" in student_range:
#                     start, end = map(int, student_range.split("-"))
#                     student_ids = list(range(start, end + 1))
#                 else:
#                     student_ids = [int(student_range.strip())]

#                 course_id = None
#                 for c in courses:
#                     if str(c["id"]) == course_input or c["code"] == course_input:
#                         course_id = c["id"]
#                         break

#                 if not course_id:
#                     st.error("❌ Course not found. Please check ID/code.")
#                 else:
#                     for sid in student_ids:
#                         payload = {"student_id": sid, "course_id": course_id}
#                         if grade_input:
#                             payload["grade"] = grade_input
#                         safe_post("/enrollments/post", payload)

#                     st.success(f"✅ Enrolled students {student_ids} to course {course_id}")
#                     st.rerun()
#             except Exception as e:
#                 st.error(f"Bulk enroll failed: {e}")

#     # ------------------------
#     # Enrollment list (visible to all)
#     # ------------------------
#     st.subheader("📋 Enrollments list")
#     query = st.text_input("Search enrollments by student or course", key="search_enr")
#     if query:
#         q = query.lower()
#         enrollments = [
#             e for e in enrollments
#             if q in student_map.get(e["student_id"], "").lower()
#             or q in course_map.get(e["course_id"], "").lower()
#         ]

#     if not enrollments:
#         st.info("No enrollments found.")
#         return

#     for e in enrollments:
#         with st.expander(f"Enroll #{e['id']}"):
#             sid, cid = e.get("student_id"), e.get("course_id")
#             st.write(
#                 f"Student: {student_map.get(sid, sid)} → Course: {course_map.get(cid, cid)} | Grade: {e.get('grade','N/A')}"
#             )

#             # Admin-only update/delete
#             if st.session_state.username == "admin":
#                 with st.form(f"update_enr_{e['id']}", clear_on_submit=True):
#                     new_grade = st.text_input("Grade", value=e.get("grade") or "", key=f"grade_{e['id']}")
#                     if st.form_submit_button("Update Grade"):
#                         data = {"student_id": sid, "course_id": cid, "grade": new_grade}
#                         r = safe_put(f"/enrollments/update/?enrollment_id={e['id']}", data)
#                         if r and r.status_code == 200:
#                             st.success("Enrollment updated")
#                             st.rerun()

#                 if st.button("❌ Delete", key=f"del_enr_{e['id']}"):
#                     r = safe_delete(f"/enrollments/delete/?enrollment_id={e['id']}")
#                     if r and r.status_code in (200, 204):
#                         st.warning("Enrollment deleted")
#                         st.rerun()




# # ------------------------
# # Login Page
# # ------------------------
# def login_page():
#     st.markdown(
#         """
#         <h1 style="text-align:center;">🎓 Student-Course Manager</h1>
#         <p style="text-align:center; font-size:16px; color:gray;">
#             Please log in to access the dashboard and manage students, courses, and enrollments.
#         </p>
#         """,
#         unsafe_allow_html=True
#     )

#     username = st.text_input("👤 Username")
#     password = st.text_input("🔑 Password", type="password")

#     if st.button("Login"):
#         if USER_CREDENTIALS.get(username) == password:
#             st.session_state.logged_in = True
#             st.session_state.username = username

#             # ✅ Store role: admin vs viewer
#             if username == "admin":
#                 st.session_state.role = "admin"
#             else:
#                 st.session_state.role = "viewer"

#             st.success(f"✅ Login successful! Logged in as {username} ({st.session_state.role})")
#             st.rerun()
#         else:
#             st.error("❌ Invalid username or password")

# import streamlit as st
# import httpx
# import pandas as pd

# # ------------------------
# # Configure API base here
# # ------------------------
# API_BASE = "http://192.168.11.104:8081/api"  # update if different

# # ------------------------
# # Dummy login credentials
# # ------------------------
# USER_CREDENTIALS = {
#     "admin": "admin123",
#     "viewer": "viewer123"
# }

# # ------------------------
# # HTTP helpers (safe)
# # ------------------------
# def safe_get(path: str):
#     url = f"{API_BASE}{path}/?skip=0&limit=100"
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             r = client.get(url)
#             if r.status_code == 200:
#                 return r.json() if r.text.strip() else []
#             else:
#                 st.error(f"GET {path} failed: {r.status_code} {r.text}")
#                 return []
#     except Exception as e:
#         st.error(f"GET {path} failed: {e}")
#         return []

# def safe_post(path: str, data: dict):
#     url = f"{API_BASE}{path}"
#     headers = {"accept": "application/json", "Content-Type": "application/json"}
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             return client.post(url=url, headers=headers, json=data)
#     except Exception as e:
#         st.error(f"POST {path} failed: {e}")
#         return None

# def safe_delete(path: str):
#     url = f"{API_BASE}{path}"
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             return client.delete(url)
#     except Exception as e:
#         st.error(f"DELETE {path} failed: {e}")
#         return None

# def safe_put(path: str, data: dict = None):
#     url = f"{API_BASE}{path}"
#     try:
#         with httpx.Client(timeout=6.0) as client:
#             return client.put(url, json=data)
#     except Exception as e:
#         st.error(f"PUT {path} failed: {e}")
#         return None


# # ------------------------
# # Dashboard
# # ------------------------
# def show_dashboard():
#     st.title("📊 Student-Course Manager — Dashboard")

#     students = safe_get("/students")
#     courses = safe_get("/courses")
#     enrollments = safe_get("/enrollments")

#     col1, col2, col3 = st.columns(3)
#     col1.metric("Students", len(students))
#     col2.metric("Courses", len(courses))
#     col3.metric("Enrollments", len(enrollments))


# # ------------------------
# # Students
# # ------------------------
# def manage_students():
#     st.title("👩‍🎓 Manage Students")

#     # Admin-only Add
#     if st.session_state.role == "admin":
#         st.subheader("➕ Add student")
#         with st.form("add_student", clear_on_submit=True):
#             name = st.text_input("Name")
#             email = st.text_input("Email")
#             roll_no = st.text_input("Roll No")
#             if st.form_submit_button("Create"):
#                 payload = {"name": name, "email": email, "roll_no": roll_no}
#                 resp = safe_post("/students/post", payload)
#                 if resp and resp.status_code in (200, 201):
#                     st.success("Student added")
#                     st.rerun()

#         # Bulk Upload
#         st.subheader("📂 Bulk Upload Students (CSV)")
#         file = st.file_uploader("Upload CSV with columns: name,email,roll_no", type="csv", key="student_upload")
#         if file:
#             df = pd.read_csv(file)
#             st.dataframe(df)
#             if st.button("Upload Students"):
#                 for _, row in df.iterrows():
#                     payload = {"name": row["name"], "email": row["email"], "roll_no": row["roll_no"]}
#                     safe_post("/students/post", payload)
#                 st.success("✅ Bulk upload completed")
#                 st.rerun()

#     # List + Search
#     st.subheader("📋 Students list")
#     students = safe_get("/students")
#     if not students:
#         st.info("No students to show.")
#         return

#     query = st.text_input("🔍 Search students by name, roll no, or email")
#     if query:
#         q = query.lower()
#         students = [s for s in students if q in s["name"].lower() or q in s["roll_no"].lower() or q in s["email"].lower()]

#     for s in students:
#         with st.expander(f"ID {s['id']} — {s['name']}"):
#             st.write(f"Roll No: {s['roll_no']} | Email: {s['email']}")

#             if st.session_state.role == "admin":
#                 if st.button("❌ Delete", key=f"del_student_{s['id']}"):
#                     r = safe_delete(f"/students/delete/?student_id={s['id']}")
#                     if r and r.status_code in (200, 204):
#                         st.warning("Student deleted")
#                         st.rerun()


# # ------------------------
# # Courses
# # ------------------------
# def manage_courses():
#     st.title("📘 Manage Courses")

#     if st.session_state.role == "admin":
#         st.subheader("➕ Add course")
#         with st.form("add_course", clear_on_submit=True):
#             code = st.text_input("Course code")
#             title = st.text_input("Title")
#             credits = st.number_input("Credits", min_value=0, step=1)
#             if st.form_submit_button("Create"):
#                 payload = {"code": code, "title": title, "credits": int(credits)}
#                 resp = safe_post("/courses/post", payload)
#                 if resp and resp.status_code in (200, 201):
#                     st.success("Course added")
#                     st.rerun()

#         # Bulk Upload
#         st.subheader("📂 Bulk Upload Courses (CSV)")
#         file = st.file_uploader("Upload CSV with columns: code,title,credits", type="csv", key="course_upload")
#         if file:
#             df = pd.read_csv(file)
#             st.dataframe(df)
#             if st.button("Upload Courses"):
#                 for _, row in df.iterrows():
#                     payload = {"code": row["code"], "title": row["title"], "credits": int(row["credits"])}
#                     safe_post("/courses/post", payload)
#                 st.success("✅ Bulk upload completed")
#                 st.rerun()

#     # List + Search
#     st.subheader("📋 Courses list")
#     courses = safe_get("/courses")
#     if not courses:
#         st.info("No courses found.")
#         return

#     query = st.text_input("🔍 Search courses by code or title")
#     if query:
#         q = query.lower()
#         courses = [c for c in courses if q in c["code"].lower() or q in c["title"].lower()]

#     for c in courses:
#         with st.expander(f"ID {c['id']} — {c['title']}"):
#             st.write(f"Code: {c['code']} | Credits: {c['credits']}")

#             if st.session_state.role == "admin":
#                 if st.button("❌ Delete", key=f"del_course_{c['id']}"):
#                     r = safe_delete(f"/courses/delete/?course_id={c['id']}")
#                     if r and r.status_code in (200, 204):
#                         st.warning("Course deleted")
#                         st.rerun()


# # ------------------------
# # Enrollments (no bulk upload)
# # ------------------------
# def manage_enrollments():
#     st.title("🎓 Manage Enrollments")

#     students = safe_get("/students")
#     courses = safe_get("/courses")
#     enrollments = safe_get("/enrollments")

#     student_map = {s["id"]: s["name"] for s in students}
#     course_map = {c["id"]: c["title"] for c in courses}

#     # ------------------------
#     # Admin-only Bulk Upload
#     # ------------------------
#     if st.session_state.role == "admin":
#         st.subheader("📂 Bulk Upload Enrollments (CSV)")
#         file = st.file_uploader(
#             "Upload CSV with columns: student_id,course_id,grade (grade optional)",
#             type="csv",
#             key="enrollment_upload"
#         )
#         if file:
#             import pandas as pd
#             df = pd.read_csv(file)
#             st.dataframe(df)

#             if st.button("Upload Enrollments"):
#                 for _, row in df.iterrows():
#                     payload = {
#                         "student_id": int(row["student_id"]),
#                         "course_id": int(row["course_id"])
#                     }
#                     if "grade" in row and not pd.isna(row["grade"]):
#                         payload["grade"] = row["grade"]

#                     safe_post("/enrollments/post", payload)

#                 st.success("✅ Bulk enrollments completed")
#                 st.rerun()

#     # ------------------------
#     # Enrollments List (for all)
#     # ------------------------
#     st.subheader("📋 Enrollments list")

#     if not enrollments:
#         st.info("No enrollments yet.")
#         return

#     for e in enrollments:
#         with st.expander(f"Enroll #{e['id']}"):
#             sid, cid = e.get("student_id"), e.get("course_id")
#             st.write(f"Student: {student_map.get(sid, sid)} → Course: {course_map.get(cid, cid)} | Grade: {e.get('grade','N/A')}")

#             if st.session_state.role == "admin":
#                 # Update grade
#                 with st.form(f"update_enr_{e['id']}", clear_on_submit=True):
#                     new_grade = st.text_input("Grade", value=e.get("grade") or "", key=f"grade_{e['id']}")
#                     if st.form_submit_button("Update Grade"):
#                         data = {"student_id": sid, "course_id": cid, "grade": new_grade}
#                         r = safe_put(f"/enrollments/update/?enrollment_id={e['id']}", data)
#                         if r and r.status_code == 200:
#                             st.success("Enrollment updated")
#                             st.rerun()

#                 # Delete enrollment
#                 if st.button("❌ Delete", key=f"del_enr_{e['id']}"):
#                     r = safe_delete(f"/enrollments/delete/?enrollment_id={e['id']}")
#                     if r and r.status_code in (200, 204):
#                         st.warning("Enrollment deleted")
#                         st.rerun()



# # ------------------------
# # Main
# # ------------------------
# def main():
#     if "logged_in" not in st.session_state:
#         st.session_state.logged_in = False

#     if not st.session_state.logged_in:
#         login_page()
#     else:
#         st.sidebar.title("Navigation")
#         st.sidebar.write(f"👋 Logged in as: **{st.session_state.username} ({st.session_state.role})**")

#         if st.sidebar.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.username = ""
#             st.session_state.role = ""
#             st.rerun()

#         page = st.sidebar.radio("Go to", ["Dashboard", "Students", "Courses", "Enrollments"])

#         if page == "Dashboard":
#             show_dashboard()
#         elif page == "Students":
#             manage_students()
#         elif page == "Courses":
#             manage_courses()
#         elif page == "Enrollments":
#             manage_enrollments()


# if __name__ == "__main__":
#     main()

import streamlit as st
import httpx
import pandas as pd

# ------------------------
# Configure API base here
# ------------------------
API_BASE = "http://192.168.11.104:8081/api"  # update if different

# ------------------------
# Dummy login credentials
# ------------------------
USER_CREDENTIALS = {
    "admin": "admin123",
    "viewer": "viewer123"
}

# ------------------------
# HTTP helpers (safe)
# ------------------------
def safe_get(path: str):
    url = f"{API_BASE}{path}/?skip=0&limit=100"
    try:
        with httpx.Client(timeout=6.0) as client:
            r = client.get(url)
            if r.status_code == 200:
                return r.json() if r.text.strip() else []
            else:
                st.error(f"GET {path} failed: {r.status_code} {r.text}")
                return []
    except Exception as e:
        st.error(f"GET {path} failed: {e}")
        return []


def safe_post(path: str, data: dict):
    url = f"{API_BASE}{path}"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    try:
        with httpx.Client(timeout=6.0) as client:
            return client.post(url=url, headers=headers, json=data)
    except Exception as e:
        st.error(f"POST {path} failed: {e}")
        return None


def safe_delete(path: str):
    url = f"{API_BASE}{path}"
    try:
        with httpx.Client(timeout=6.0) as client:
            return client.delete(url)
    except Exception as e:
        st.error(f"DELETE {path} failed: {e}")
        return None


def safe_put(path: str, data: dict = None):
    url = f"{API_BASE}{path}"
    try:
        with httpx.Client(timeout=6.0) as client:
            return client.put(url, json=data)
    except Exception as e:
        st.error(f"PUT {path} failed: {e}")
        return None

# ------------------------
# Login Page
# ------------------------
def login_page():
    st.markdown(
        """
        <h1 style="text-align:center;">🎓 Student-Course Manager</h1>
        <p style="text-align:center; font-size:16px; color:gray;">
            Please log in to access the dashboard and manage students, courses, and enrollments.
        </p>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if USER_CREDENTIALS.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = "admin" if username == "admin" else "viewer"
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# ------------------------
# Dashboard
# ------------------------
def show_dashboard():
    st.title("📊 Student-Course Manager — Dashboard")

    students = safe_get("/students")
    courses = safe_get("/courses")
    enrollments = safe_get("/enrollments")

    col1, col2, col3 = st.columns(3)
    col1.metric("Students", len(students))
    col2.metric("Courses", len(courses))
    col3.metric("Enrollments", len(enrollments))

    st.markdown("---")
    st.subheader("Recent enrollments (latest 5)")
    if enrollments:
        student_map = {s["id"]: s.get("name", str(s["id"])) for s in students}
        course_map = {c["id"]: c.get("title", c.get("code", str(c["id"]))) for c in courses}
        for e in enrollments[-5:][::-1]:
            sid, cid = e.get("student_id"), e.get("course_id")
            grade = e.get("grade") or "N/A"
            st.write(f"- #{e.get('id')} — **{student_map.get(sid, sid)}** → **{course_map.get(cid, cid)}** (grade: {grade})")
    else:
        st.info("No enrollments yet.")

# ------------------------
# Students
# ------------------------
def manage_students():
    st.title("👩‍🎓 Manage Students")

    if st.session_state.role == "admin":
        st.subheader("➕ Add student")
        with st.form("add_student", clear_on_submit=True):
            name = st.text_input("Name")
            email = st.text_input("Email")
            roll_no = st.text_input("Roll No")
            if st.form_submit_button("Create"):
                payload = {"name": name, "email": email, "roll_no": roll_no}
                resp = safe_post("/students/post", payload)
                if resp and resp.status_code in (200, 201):
                    st.success("Student added")
                    st.rerun()

        # Bulk upload CSV
        st.subheader("📤 Bulk Upload Students (CSV)")
        csv_file = st.file_uploader("Upload CSV with columns: name,email,roll_no", type="csv", key="student_upload")
        if csv_file:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                payload = {"name": row["name"], "email": row["email"], "roll_no": row["roll_no"]}
                safe_post("/students/post", payload)
            st.success("✅ Bulk students uploaded!")
            st.rerun()

    st.subheader("📋 Students list")
    students = safe_get("/students")
    if not students:
        st.info("No students to show.")
        return

    query = st.text_input("Search students by name, roll no, or email", key="student_search")
    if query:
        q = query.lower()
        students = [s for s in students if q in s["name"].lower() or q in s["roll_no"].lower() or q in s["email"].lower()]

    for s in students:
        with st.expander(f"ID {s['id']} — {s['name']}"):
            st.write(f"Roll No: {s['roll_no']} | Email: {s['email']}")

            if st.session_state.role == "admin":
                with st.form(f"update_student_{s['id']}", clear_on_submit=True):
                    new_name = st.text_input("Edit name", value=s["name"], key=f"name_{s['id']}")
                    new_email = st.text_input("Edit email", value=s["email"], key=f"email_{s['id']}")
                    new_roll = st.text_input("Edit roll no", value=s["roll_no"], key=f"roll_{s['id']}")
                    if st.form_submit_button("Update"):
                        data = {"name": new_name, "email": new_email, "roll_no": new_roll}
                        r = safe_put(f"/students/update/?student_id={s['id']}", data)
                        if r and r.status_code == 200:
                            st.success("Student updated")
                            st.rerun()

                if st.button("❌ Delete", key=f"del_student_{s['id']}"):
                    r = safe_delete(f"/students/delete/?student_id={s['id']}")
                    if r and r.status_code in (200, 204):
                        st.warning("Student deleted")
                        st.rerun()

# ------------------------
# Courses
# ------------------------
def manage_courses():
    st.title("📘 Manage Courses")

    if st.session_state.role == "admin":
        st.subheader("➕ Add course")
        with st.form("add_course", clear_on_submit=True):
            code = st.text_input("Course code")
            title = st.text_input("Title")
            credits = st.number_input("Credits", min_value=0, step=1)
            if st.form_submit_button("Create"):
                payload = {"code": code, "title": title, "credits": int(credits)}
                resp = safe_post("/courses/post", payload)
                if resp and resp.status_code in (200, 201):
                    st.success("Course added")
                    st.rerun()

        st.subheader("📤 Bulk Upload Courses (CSV)")
        csv_file = st.file_uploader("Upload CSV with columns: code,title,credits", type="csv", key="course_upload")
        if csv_file:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                payload = {"code": row["code"], "title": row["title"], "credits": int(row["credits"])}
                safe_post("/courses/post", payload)
            st.success("✅ Bulk courses uploaded!")
            st.rerun()

    st.subheader("📋 Courses list")
    courses = safe_get("/courses")
    if not courses:
        st.info("No courses found.")
        return

    query = st.text_input("Search courses by code or title", key="course_search")
    if query:
        q = query.lower()
        courses = [c for c in courses if q in c["code"].lower() or q in c["title"].lower()]

    for c in courses:
        with st.expander(f"ID {c['id']} — {c['title']}"):
            st.write(f"Code: {c['code']} | Credits: {c['credits']}")

            if st.session_state.role == "admin":
                with st.form(f"update_course_{c['id']}", clear_on_submit=True):
                    new_code = st.text_input("Edit code", value=c["code"], key=f"code_{c['id']}")
                    new_title = st.text_input("Edit title", value=c["title"], key=f"title_{c['id']}")
                    new_credits = st.number_input("Edit credits", value=c["credits"], step=1, key=f"credits_{c['id']}")
                    if st.form_submit_button("Update"):
                        data = {"code": new_code, "title": new_title, "credits": int(new_credits)}
                        r = safe_put(f"/courses/update/?course_id={c['id']}", data)
                        if r and r.status_code == 200:
                            st.success("Course updated")
                            st.rerun()

                if st.button("❌ Delete", key=f"del_course_{c['id']}"):
                    r = safe_delete(f"/courses/delete/?course_id={c['id']}")
                    if r and r.status_code in (200, 204):
                        st.warning("Course deleted")
                        st.rerun()

# ------------------------
# Enrollments
# ------------------------
def manage_enrollments():
    st.title("🎓 Manage Enrollments")

    students = safe_get("/students")
    courses = safe_get("/courses")
    enrollments = safe_get("/enrollments")

    student_map = {s["id"]: s["name"] for s in students}
    course_map = {c["id"]: c["title"] for c in courses}

    if st.session_state.role == "admin":
        st.subheader("➕ Enroll a student")
        with st.form("add_enrollment", clear_on_submit=True):
            sid = st.selectbox("Student", options=[s["id"] for s in students], format_func=lambda x: student_map[x], key="single_enroll_student")
            cid = st.selectbox("Course", options=[c["id"] for c in courses], format_func=lambda x: course_map[x], key="single_enroll_course")
            grade = st.text_input("Grade (optional)", key="single_enroll_grade")
            if st.form_submit_button("Enroll"):
                payload = {"student_id": sid, "course_id": cid}
                if grade:
                    payload["grade"] = grade
                resp = safe_post("/enrollments/post", payload)
                if resp and resp.status_code in (200, 201):
                    st.success("Enrolled")
                    st.rerun()

        st.subheader("📤 Bulk Upload Enrollments (CSV)")
        csv_file = st.file_uploader("Upload CSV with columns: student_id,course_id,grade(optional)", type="csv", key="enroll_upload")
        if csv_file:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                payload = {"student_id": int(row["student_id"]), "course_id": int(row["course_id"])}
                if "grade" in row and not pd.isna(row["grade"]):
                    payload["grade"] = row["grade"]
                safe_post("/enrollments/post", payload)
            st.success("✅ Bulk enrollments uploaded!")
            st.rerun()

        st.subheader("📌 Range Enroll (e.g., 1-10 to Course 1001)")
        student_range = st.text_input("Enter Student ID Range (e.g., 1-10)", key="range_enroll_students")
        course_id = st.selectbox("Course", options=[c["id"] for c in courses], format_func=lambda x: course_map[x], key="range_enroll_course")
        if st.button("Enroll Range"):
            try:
                start, end = map(int, student_range.split("-"))
                for sid in range(start, end + 1):
                    payload = {"student_id": sid, "course_id": course_id}
                    safe_post("/enrollments/post", payload)
                st.success(f"Enrolled students {start} to {end} into course {course_id}")
                st.rerun()
            except Exception as e:
                st.error(f"Invalid range format: {e}")

    st.subheader("📋 Enrollments list")
    query = st.text_input("Search enrollments by student or course", key="enroll_search")
    if query:
        q = query.lower()
        enrollments = [
            e for e in enrollments
            if q in student_map.get(e["student_id"], "").lower()
            or q in course_map.get(e["course_id"], "").lower()
        ]

    if not enrollments:
        st.info("No enrollments found.")
        return

    for e in enrollments:
        with st.expander(f"Enroll #{e['id']}"):
            sid, cid = e.get("student_id"), e.get("course_id")
            st.write(f"Student: {student_map.get(sid, sid)} → Course: {course_map.get(cid, cid)} | Grade: {e.get('grade','N/A')}")

            if st.session_state.role == "admin":
                with st.form(f"update_enr_{e['id']}", clear_on_submit=True):
                    new_grade = st.text_input("Grade", value=e.get("grade") or "", key=f"grade_{e['id']}")
                    if st.form_submit_button("Update Grade"):
                        data = {"student_id": sid, "course_id": cid, "grade": new_grade}
                        r = safe_put(f"/enrollments/update/?enrollment_id={e['id']}", data)
                        if r and r.status_code == 200:
                            st.success("Enrollment updated")
                            st.rerun()

                if st.button("❌ Delete", key=f"del_enr_{e['id']}"):
                    r = safe_delete(f"/enrollments/delete/?enrollment_id={e['id']}")
                    if r and r.status_code in (200, 204):
                        st.warning("Enrollment deleted")
                        st.rerun()

# ------------------------
# Main
# ------------------------
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.title("Navigation")
        st.sidebar.write(f"👋 Logged in as: **{st.session_state.username} ({st.session_state.role})**")

        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.rerun()

        page = st.sidebar.radio("Go to", ["Dashboard", "Students", "Courses", "Enrollments"])

        if page == "Dashboard":
            show_dashboard()
        elif page == "Students":
            manage_students()
        elif page == "Courses":
            manage_courses()
        elif page == "Enrollments":
            manage_enrollments()


if __name__ == "__main__":
    main()



