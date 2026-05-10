import streamlit as st
import pandas as pd
from utils.styles import GLOBAL_CSS, topbar
from database import get_all_employees, get_dept_stats, get_predictions


def show(go, go_back, logout):
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    name = st.session_state.get("name", "Manager")
    st.markdown(topbar("Dashboard", name, "management"), unsafe_allow_html=True)

    pad = st.columns([0.03, 0.94, 0.03])
    with pad[1]:
        # Nav bar
        n1, n2, n3, n4, _, lc = st.columns([1.5, 1.8, 1.8, 2, 3, 1.5])
        with n1:
            if st.button("← Back", key="md_back"):
                go_back()
        with n2:
            if st.button("👥 Employees", key="md_emp"):
                go("mgmt_employees")
        with n3:
            if st.button("📊 Analytics", key="md_ana"):
                go("mgmt_analytics")
        with n4:
            if st.button("🎯 Predict", key="md_pred"):
                go("mgmt_predict")
        with lc:
            st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
            if st.button("Sign Out", key="md_logout"):
                logout()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="page-title">Management Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Overview of all employees and performance metrics</div>', unsafe_allow_html=True)

        # ── Stats ─────────────────────────────────────────────────────────────
        all_emps   = get_all_employees()
        dept_stats = get_dept_stats()
        preds      = get_predictions()

        total      = len(all_emps)
        dept_count = len(dept_stats)
        avg_sat    = round(sum(e.get("satisfaction_score",0) or 0 for e in all_emps) / total, 2) if total else 0
        pred_count = len(preds)

        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-card purple">
                <div class="stat-label">Total Employees</div>
                <div class="stat-value">{total}</div>
                <div class="stat-sub">Registered in system</div>
            </div>
            <div class="stat-card teal">
                <div class="stat-label">Departments</div>
                <div class="stat-value">{dept_count}</div>
                <div class="stat-sub">Active departments</div>
            </div>
            <div class="stat-card amber">
                <div class="stat-label">Avg Satisfaction</div>
                <div class="stat-value">{avg_sat}</div>
                <div class="stat-sub">Out of 5.0</div>
            </div>
            <div class="stat-card rose">
                <div class="stat-label">Predictions Run</div>
                <div class="stat-value">{pred_count}</div>
                <div class="stat-sub">Total predictions</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Quick nav cards ───────────────────────────────────────────────────
        st.markdown('<div class="sec-title">⚡ Quick Access</div>', unsafe_allow_html=True)
        q1, q2, q3 = st.columns(3)

        cards = [
            (q1, "👥", "Employee Records", "View, filter, add, edit and delete employees", "mgmt_employees"),
            (q2, "🎯", "Performance Prediction", "Predict employee performance using ML model", "mgmt_predict"),
            (q3, "📊", "Analytics & Reports", "Department charts, top performers, trend reports", "mgmt_analytics"),
        ]
        for col, icon, title, desc, dest in cards:
            with col:
                st.markdown(f"""
                <div class="info-card" style="text-align:center;min-height:140px;">
                    <div style="font-size:2rem;margin-bottom:0.5rem;">{icon}</div>
                    <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;font-size:1rem;">{title}</div>
                    <div style="color:rgba(255,255,255,0.35);font-size:0.8rem;margin-top:0.3rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Open →", key=f"qa_{dest}", use_container_width=True):
                    go(dest)

        # ── Department summary ────────────────────────────────────────────────
        if dept_stats:
            st.markdown('<div class="sec-title">🏢 Department Summary</div>', unsafe_allow_html=True)
            df = pd.DataFrame(dept_stats)
            df = df.rename(columns={
                "department":"Department","total":"Employees",
                "avg_salary":"Avg Salary","avg_satisfaction":"Avg Satisfaction",
                "avg_training":"Avg Training Hrs","avg_attendance":"Avg Attendance %"
            })
            for col in ["Avg Salary","Avg Satisfaction","Avg Training Hrs","Avg Attendance %"]:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: round(x,2) if x else 0)
            st.dataframe(df, use_container_width=True, hide_index=True)

        # ── Recent predictions ────────────────────────────────────────────────
        if preds:
            st.markdown('<div class="sec-title">📋 Recent Predictions</div>', unsafe_allow_html=True)
            recent = pd.DataFrame(preds[:10])[["predicted_at","employee_id","predicted_score","category","department"]]
            recent.columns = ["Date","Employee ID","Score","Category","Department"]
            st.dataframe(recent, use_container_width=True, hide_index=True)
