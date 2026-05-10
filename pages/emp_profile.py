import streamlit as st
from utils.styles import GLOBAL_CSS, topbar
from database import get_employee_by_id, update_employee

DEPTS = ["IT","Finance","Engineering","HR","Sales","Marketing","Operations","Legal","Customer Support"]
JOBS  = ["Analyst","Developer","Specialist","Engineer","Manager","Consultant","Technician","Intern"]
EDUS  = ["High School","Bachelor","Master","PhD"]

def _idx(lst, val):
    try: return lst.index(val)
    except: return 0


def show(go, go_back, logout):
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    name   = st.session_state.get("name", "Employee")
    emp_id = st.session_state.get("employee_id", "")

    st.markdown(topbar("My Profile", name, "employee"), unsafe_allow_html=True)

    pad = st.columns([0.03, 0.94, 0.03])
    with pad[1]:
        bc, _, lc = st.columns([1.5, 8, 1.5])
        with bc:
            if st.button("← Back", key="prof_back"):
                go_back()
        with lc:
            st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
            if st.button("Sign Out", key="prof_logout"):
                logout()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="page-title">My Profile</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Update your information — changes are saved to the database</div>', unsafe_allow_html=True)

        emp = get_employee_by_id(emp_id) or {}

        with st.form("profile_form"):
            st.markdown('<div class="sec-title">👤 Personal Information</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                full_name = st.text_input("Full Name", emp.get("full_name",""))
                email     = st.text_input("Email", emp.get("email",""))
            with c2:
                contact   = st.text_input("Contact", emp.get("contact",""))
                age       = st.number_input("Age", 18, 65, int(emp.get("age") or 25))
            with c3:
                gender    = st.selectbox("Gender", ["Male","Female","Other"],
                                         index=_idx(["Male","Female","Other"], emp.get("gender","Male")))
                education = st.selectbox("Education Level", EDUS,
                                         index=_idx(EDUS, emp.get("education_level","Bachelor")))

            st.markdown('<div class="sec-title">💼 Work Details</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                department  = st.selectbox("Department", DEPTS, index=_idx(DEPTS, emp.get("department","IT")))
                designation = st.selectbox("Designation", JOBS,  index=_idx(JOBS,  emp.get("designation","Analyst")))
            with c2:
                salary       = st.number_input("Monthly Salary", 3000, 100000, int(emp.get("salary") or 6000), step=500)
                experience   = st.number_input("Experience (Years)", 0, 40, int(emp.get("experience") or 0))
            with c3:
                working_hours  = st.number_input("Working Hours/Week", 20.0, 80.0, float(emp.get("working_hours") or 40.0), step=0.5)
                overtime_hours = st.number_input("Overtime Hours/Month", 0.0, 100.0, float(emp.get("overtime_hours") or 0.0), step=0.5)

            st.markdown('<div class="sec-title">📊 Performance Data</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                attendance_pct     = st.number_input("Attendance %", 0.0, 100.0, float(emp.get("attendance_pct") or 90.0), step=0.5)
                projects_completed = st.number_input("Projects Completed", 0, 500, int(emp.get("projects_completed") or 0))
            with c2:
                training_hours = st.number_input("Training Hours (Annual)", 0.0, 500.0, float(emp.get("training_hours") or 0.0))
                promotions     = st.number_input("Promotions", 0, 10, int(emp.get("promotions") or 0))
            with c3:
                previous_rating    = st.slider("Previous Rating", 1.0, 5.0, float(emp.get("previous_rating") or 3.0), 0.1)
                satisfaction_score = st.slider("Satisfaction Score", 1.0, 5.0, float(emp.get("satisfaction_score") or 3.0), 0.1)

            st.write("")
            saved = st.form_submit_button("💾  Save Changes", use_container_width=True)

        if saved:
            update_employee(emp_id, {
                "full_name": full_name, "email": email, "contact": contact,
                "age": age, "gender": gender, "department": department,
                "designation": designation, "education_level": education,
                "salary": salary, "experience": experience,
                "attendance_pct": attendance_pct, "projects_completed": projects_completed,
                "working_hours": working_hours, "overtime_hours": overtime_hours,
                "training_hours": training_hours, "promotions": promotions,
                "previous_rating": previous_rating, "satisfaction_score": satisfaction_score,
            })
            st.session_state.name = full_name
            st.success("✅ Profile updated successfully!")
            st.rerun()

        if emp.get("updated_at"):
            st.caption(f"Last updated: {emp['updated_at']}")
