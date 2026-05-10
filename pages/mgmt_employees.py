import streamlit as st
import pandas as pd
from utils.styles import GLOBAL_CSS, topbar
from database import get_all_employees, delete_employee, update_employee, get_departments

DEPTS = ["IT","Finance","Engineering","HR","Sales","Marketing","Operations","Legal","Customer Support"]
JOBS  = ["Analyst","Developer","Specialist","Engineer","Manager","Consultant","Technician","Intern"]
EDUS  = ["High School","Bachelor","Master","PhD"]
DEPT_ICONS = {"IT":"💻","Finance":"💰","Engineering":"⚙️","HR":"🧑‍💼","Sales":"📈",
              "Marketing":"📣","Operations":"🔧","Legal":"⚖️","Customer Support":"🎧"}

def _idx(lst, val):
    try: return lst.index(val)
    except: return 0


def show(go, go_back, logout):
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    name = st.session_state.get("name","Manager")
    st.markdown(topbar("Employee Records", name, "management"), unsafe_allow_html=True)

    pad = st.columns([0.03, 0.94, 0.03])
    with pad[1]:
        n1, n2, n3, n4, _, lc = st.columns([1.5, 1.8, 1.8, 2, 3, 1.5])
        with n1:
            if st.button("← Back", key="me_back"): go_back()
        with n2:
            if st.button("🏠 Dashboard", key="me_dash"): go("mgmt_dashboard")
        with n3:
            if st.button("🎯 Predict", key="me_pred"): go("mgmt_predict")
        with n4:
            if st.button("📊 Analytics", key="me_ana"): go("mgmt_analytics")
        with lc:
            st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
            if st.button("Sign Out", key="me_logout"): logout()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="page-title">Employee Records</div>', unsafe_allow_html=True)

        # ── Department cards ──────────────────────────────────────────────────
        if "mgmt_dept" not in st.session_state:
            st.session_state.mgmt_dept = "All"

        all_emps = get_all_employees()
        dept_counts = {}
        for e in all_emps:
            d = e.get("department","Unknown")
            dept_counts[d] = dept_counts.get(d, 0) + 1

        st.markdown('<div class="sec-title">🏢 Filter by Department</div>', unsafe_allow_html=True)

        dept_list = ["All"] + sorted(dept_counts.keys())
        rows = [dept_list[i:i+5] for i in range(0, len(dept_list), 5)]
        for row in rows:
            cols = st.columns(len(row))
            for i, dept in enumerate(row):
                with cols[i]:
                    icon  = "🌐" if dept == "All" else DEPT_ICONS.get(dept,"🏢")
                    count = len(all_emps) if dept == "All" else dept_counts.get(dept, 0)
                    sel   = st.session_state.mgmt_dept == dept
                    border = "2px solid #6c63ff" if sel else "1px solid rgba(255,255,255,0.08)"
                    bg     = "rgba(108,99,255,0.12)" if sel else "rgba(255,255,255,0.03)"
                    st.markdown(f"""
                    <div style="background:{bg};border:{border};border-radius:12px;
                                padding:0.9rem;text-align:center;margin-bottom:0.3rem;">
                        <div style="font-size:1.4rem;">{icon}</div>
                        <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.8rem;color:white;">{dept}</div>
                        <div style="font-size:0.72rem;color:rgba(255,255,255,0.35);">{count} emp</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Select", key=f"dep_{dept}_{i}"):
                        st.session_state.mgmt_dept = dept
                        st.rerun()

        # ── Search + filters ──────────────────────────────────────────────────
        st.markdown('<div class="sec-title">🔍 Search & Manage</div>', unsafe_allow_html=True)
        sc1, sc2 = st.columns([3, 1])
        with sc1:
            search = st.text_input("Search by Name, ID or Department", placeholder="Type to search...")
        with sc2:
            st.write("")
            if st.button("➕ Add New Employee", key="add_emp_btn", use_container_width=True):
                go("emp_register")

        # ── Filtered employee list ────────────────────────────────────────────
        dept_filter = None if st.session_state.mgmt_dept == "All" else st.session_state.mgmt_dept
        filtered = get_all_employees(department=dept_filter, search=search if search else None)

        st.caption(f"Showing {len(filtered)} employee(s)" + (f" in {dept_filter}" if dept_filter else ""))

        if not filtered:
            st.info("No employees found.")
        else:
            disp_cols = ["employee_id","full_name","department","designation","age","salary",
                         "attendance_pct","projects_completed","satisfaction_score","updated_at"]
            disp_rename = {
                "employee_id":"ID","full_name":"Name","department":"Dept","designation":"Role",
                "age":"Age","salary":"Salary","attendance_pct":"Attend %",
                "projects_completed":"Projects","satisfaction_score":"Satisfaction","updated_at":"Updated"
            }
            df = pd.DataFrame(filtered)
            show_df = df[[c for c in disp_cols if c in df.columns]].rename(columns=disp_rename)
            st.dataframe(show_df, use_container_width=True, hide_index=True)

        # ── Edit / Delete ─────────────────────────────────────────────────────
        st.markdown('<div class="sec-title">✏️ Edit / Delete Employee</div>', unsafe_allow_html=True)

        if filtered:
            emp_options = {f"{e['full_name']} ({e['employee_id']})": e for e in filtered}
            chosen_label = st.selectbox("Select employee to edit or delete", list(emp_options.keys()))
            emp = emp_options[chosen_label]

            tab_edit, tab_del = st.tabs(["✏️ Edit Record", "🗑️ Delete Employee"])

            with tab_edit:
                with st.form("edit_emp_form"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        full_name    = st.text_input("Full Name", emp.get("full_name",""))
                        email        = st.text_input("Email", emp.get("email",""))
                        contact      = st.text_input("Contact", emp.get("contact",""))
                        age          = st.number_input("Age", 18, 65, int(emp.get("age") or 25))
                    with c2:
                        gender       = st.selectbox("Gender", ["Male","Female","Other"], index=_idx(["Male","Female","Other"], emp.get("gender","Male")))
                        department   = st.selectbox("Department", DEPTS, index=_idx(DEPTS, emp.get("department","IT")))
                        designation  = st.selectbox("Designation", JOBS,  index=_idx(JOBS,  emp.get("designation","Analyst")))
                        education    = st.selectbox("Education", EDUS,  index=_idx(EDUS,  emp.get("education_level","Bachelor")))
                    with c3:
                        salary       = st.number_input("Salary", 3000, 100000, int(emp.get("salary") or 6000), step=500)
                        experience   = st.number_input("Experience (yrs)", 0, 40, int(emp.get("experience") or 0))
                        attendance_pct      = st.number_input("Attendance %", 0.0, 100.0, float(emp.get("attendance_pct") or 90.0))
                        projects_completed  = st.number_input("Projects", 0, 500, int(emp.get("projects_completed") or 0))
                        working_hours       = st.number_input("Work Hrs/Wk", 20.0, 80.0, float(emp.get("working_hours") or 40.0))
                        overtime_hours      = st.number_input("Overtime Hrs", 0.0, 100.0, float(emp.get("overtime_hours") or 0.0))
                        training_hours      = st.number_input("Training Hrs", 0.0, 500.0, float(emp.get("training_hours") or 0.0))
                        promotions          = st.number_input("Promotions", 0, 10, int(emp.get("promotions") or 0))
                        previous_rating     = st.slider("Prev Rating", 1.0, 5.0, float(emp.get("previous_rating") or 3.0), 0.1)
                        satisfaction_score  = st.slider("Satisfaction", 1.0, 5.0, float(emp.get("satisfaction_score") or 3.0), 0.1)

                    if st.form_submit_button("💾 Save Changes", use_container_width=True):
                        update_employee(emp["employee_id"], {
                            "full_name":full_name,"email":email,"contact":contact,"age":age,
                            "gender":gender,"department":department,"designation":designation,
                            "education_level":education,"salary":salary,"experience":experience,
                            "attendance_pct":attendance_pct,"projects_completed":projects_completed,
                            "working_hours":working_hours,"overtime_hours":overtime_hours,
                            "training_hours":training_hours,"promotions":promotions,
                            "previous_rating":previous_rating,"satisfaction_score":satisfaction_score,
                        })
                        st.success(f"✅ {full_name}'s record updated.")
                        st.rerun()

            with tab_del:
                st.warning(f"⚠️ You are about to permanently delete **{emp['full_name']}** ({emp['employee_id']}). This cannot be undone.")
                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                if st.button(f"🗑️ Delete {emp['full_name']}", key="del_btn", use_container_width=True):
                    delete_employee(emp["employee_id"])
                    st.success(f"Deleted {emp['full_name']}.")
                    st.session_state.mgmt_dept = "All"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
