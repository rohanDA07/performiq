import streamlit as st
from utils.styles import GLOBAL_CSS, topbar
from database import get_employee_by_id, get_predictions


def show(go, go_back, logout):
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    name    = st.session_state.get("name", "Employee")
    emp_id  = st.session_state.get("employee_id", "")
    initials = "".join([w[0].upper() for w in name.split()[:2]])

    st.markdown(topbar("My Dashboard", name, "employee"), unsafe_allow_html=True)

    pad = st.columns([0.03, 0.94, 0.03])
    with pad[1]:
        # ── Top actions ───────────────────────────────────────────────────────
        ac1, ac2, ac3, _, logout_col = st.columns([2, 2, 2, 4, 1.5])
        with ac1:
            if st.button("← Back", key="emp_dash_back"):
                go_back()
        with ac2:
            if st.button("✏️ Edit Profile", key="go_profile"):
                go("emp_profile")
        with ac3:
            if st.button("🎯 My Prediction", key="go_pred"):
                go("emp_predict")
        with logout_col:
            st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
            if st.button("Sign Out", key="emp_logout"):
                logout()
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Welcome ───────────────────────────────────────────────────────────
        emp = get_employee_by_id(emp_id) or {}

        dept = emp.get("department", "—")
        desig = emp.get("designation", "—")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a1040,#0d2a3a);
                    border:1px solid rgba(108,99,255,0.2);border-radius:20px;
                    padding:2rem 2.5rem;margin:1.5rem 0;position:relative;overflow:hidden;">
            <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;
                        background:radial-gradient(circle,rgba(108,99,255,0.12),transparent 70%);
                        border-radius:50%;"></div>
            <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:white;">
                Hello, {name.split()[0]} 👋
            </div>
            <div style="color:rgba(255,255,255,0.45);margin-top:0.3rem;font-size:0.88rem;">
                {desig} &nbsp;·&nbsp; {dept} &nbsp;·&nbsp; ID: {emp_id}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Quick stats ───────────────────────────────────────────────────────
        sat   = emp.get("satisfaction_score", "—")
        att   = emp.get("attendance_pct", "—")
        proj  = emp.get("projects_completed", "—")
        exp   = emp.get("experience", "—")

        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-card teal">
                <div class="stat-label">Satisfaction</div>
                <div class="stat-value">{sat}</div>
                <div class="stat-sub">Out of 5.0</div>
            </div>
            <div class="stat-card purple">
                <div class="stat-label">Attendance</div>
                <div class="stat-value">{att}%</div>
                <div class="stat-sub">This period</div>
            </div>
            <div class="stat-card amber">
                <div class="stat-label">Projects</div>
                <div class="stat-value">{proj}</div>
                <div class="stat-sub">Completed</div>
            </div>
            <div class="stat-card green">
                <div class="stat-label">Experience</div>
                <div class="stat-value">{exp} yr</div>
                <div class="stat-sub">Total experience</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Quick navigation cards ────────────────────────────────────────────
        st.markdown('<div class="sec-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
        q1, q2 = st.columns(2)

        with q1:
            st.markdown("""
            <div class="info-card" style="border-color:rgba(108,99,255,0.2);">
                <div style="font-size:1.8rem;margin-bottom:0.6rem;">✏️</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;font-size:1rem;">Update My Profile</div>
                <div style="color:rgba(255,255,255,0.4);font-size:0.82rem;margin-top:0.3rem;">
                    Edit your personal details, work info and more
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Go to Profile →", key="qa_profile", use_container_width=True):
                go("emp_profile")

        with q2:
            st.markdown("""
            <div class="info-card" style="border-color:rgba(62,207,207,0.2);">
                <div style="font-size:1.8rem;margin-bottom:0.6rem;">🎯</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;font-size:1rem;">Check My Performance</div>
                <div style="color:rgba(255,255,255,0.4);font-size:0.82rem;margin-top:0.3rem;">
                    View ML-predicted score and improvement tips
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Predict Now →", key="qa_predict", use_container_width=True):
                go("emp_predict")

        # ── Recent predictions ────────────────────────────────────────────────
        records = get_predictions(emp_id)
        if records:
            st.markdown('<div class="sec-title">📋 Recent Predictions</div>', unsafe_allow_html=True)
            for r in records[:3]:
                cat = r["category"]
                color = "#34d399" if "Excellent" in cat else "#fbbf24" if "Average" in cat else "#fb7185"
                st.markdown(f"""
                <div class="info-card" style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="color:{color};font-weight:700;font-family:'Syne',sans-serif;">{cat}</span>
                        <div style="color:rgba(255,255,255,0.35);font-size:0.78rem;margin-top:0.2rem;">{r['predicted_at']}</div>
                    </div>
                    <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:white;">{r['predicted_score']}</div>
                </div>
                """, unsafe_allow_html=True)
