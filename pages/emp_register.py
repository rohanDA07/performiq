import streamlit as st
from utils.styles import GLOBAL_CSS, topbar
from database import register_employee

CSS = GLOBAL_CSS


def show(go, go_back):
    st.markdown(CSS, unsafe_allow_html=True)

    st.markdown(topbar("Employee Registration", "New Employee", "employee"), unsafe_allow_html=True)

    pad = st.columns([0.03, 0.94, 0.03])
    with pad[1]:
        bc, _ = st.columns([1, 8])
        with bc:
            if st.button("← Back", key="reg_back"):
                go_back()

        st.markdown('<div class="page-title">Employee Registration</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Fill in all details to create your account</div>', unsafe_allow_html=True)

        with st.form("register_form", clear_on_submit=False):

            # ── Account credentials ───────────────────────────────────────────
            st.markdown('<div class="sec-title">🔐 Account Credentials</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                employee_id = st.text_input("Employee ID *", placeholder="EMP005")
            with c2:
                username    = st.text_input("Username *", placeholder="john_doe")
            with c3:
                password    = st.text_input("Password *", type="password", placeholder="Min 6 chars")

            # ── Personal info ─────────────────────────────────────────────────
            st.markdown('<div class="sec-title">👤 Personal Information</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                full_name = st.text_input("Full Name *", placeholder="John Doe")
                email     = st.text_input("Email", placeholder="john@company.com")
            with c2:
                contact   = st.text_input("Contact Number", placeholder="9876543210")
                age       = st.number_input("Age *", 18, 65, 28)
            with c3:
                gender    = st.selectbox("Gender *", ["Male", "Female", "Other"])
                education = st.selectbox("Education Level *", ["High School", "Bachelor", "Master", "PhD"])

            # ── Work details ──────────────────────────────────────────────────
            st.markdown('<div class="sec-title">💼 Work Details</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                department   = st.selectbox("Department *", [
                    "IT","Finance","Engineering","HR","Sales",
                    "Marketing","Operations","Legal","Customer Support"
                ])
                designation  = st.selectbox("Designation *", [
                    "Analyst","Developer","Specialist","Engineer",
                    "Manager","Consultant","Technician","Intern"
                ])
            with c2:
                salary       = st.number_input("Monthly Salary (₹/$) *", 3000, 100000, 6000, step=500)
                experience   = st.number_input("Experience (Years) *", 0, 40, 2)
            with c3:
                working_hours   = st.number_input("Working Hours/Week *", 20.0, 80.0, 40.0, step=0.5)
                overtime_hours  = st.number_input("Overtime Hours/Month", 0.0, 100.0, 0.0, step=0.5)

            # ── Performance data ──────────────────────────────────────────────
            st.markdown('<div class="sec-title">📊 Performance Data</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                attendance_pct      = st.number_input("Attendance % *", 0.0, 100.0, 90.0, step=0.5)
                projects_completed  = st.number_input("Projects Completed *", 0, 200, 5)
            with c2:
                training_hours  = st.number_input("Training Hours (Annual)", 0.0, 500.0, 20.0, step=1.0)
                promotions      = st.number_input("Promotions Received", 0, 10, 0)
            with c3:
                previous_rating   = st.slider("Previous Rating (1-5)", 1.0, 5.0, 3.0, step=0.1)
                satisfaction_score = st.slider("Satisfaction Score (1-5)", 1.0, 5.0, 3.0, step=0.1)

            st.write("")
            submitted = st.form_submit_button("✅  Create My Account", use_container_width=True)

        if submitted:
            errors = []
            if not employee_id: errors.append("Employee ID is required.")
            if not username:    errors.append("Username is required.")
            if not password or len(password) < 6: errors.append("Password must be at least 6 characters.")
            if not full_name:   errors.append("Full Name is required.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                ok, msg = register_employee({
                    "employee_id": employee_id.strip(),
                    "username": username.strip(),
                    "password": password,
                    "full_name": full_name.strip(),
                    "email": email.strip(),
                    "contact": contact.strip(),
                    "age": age, "gender": gender,
                    "department": department, "designation": designation,
                    "education_level": education,
                    "salary": salary, "experience": experience,
                    "attendance_pct": attendance_pct,
                    "projects_completed": projects_completed,
                    "working_hours": working_hours,
                    "overtime_hours": overtime_hours,
                    "training_hours": training_hours,
                    "promotions": promotions,
                    "previous_rating": previous_rating,
                    "satisfaction_score": satisfaction_score,
                })
                if ok:
                    st.success("🎉 Account created successfully! Please sign in.")
                    st.balloons()
                    import time; time.sleep(2)
                    go("emp_login")
                else:
                    st.error(msg)
