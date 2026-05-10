import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import GLOBAL_CSS, topbar
from database import get_all_employees, get_dept_stats, get_predictions


def show(go_fn, go_back, logout):
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    name = st.session_state.get("name", "Manager")
    st.markdown(topbar("Analytics", name, "management"), unsafe_allow_html=True)

    pad = st.columns([0.03, 0.94, 0.03])
    with pad[1]:
        n1, n2, n3, n4, _, lc = st.columns([1.5, 1.8, 1.8, 2, 3, 1.5])
        with n1:
            if st.button("← Back", key="ma_back"): go_back()
        with n2:
            if st.button("🏠 Dashboard", key="ma_dash"): go_fn("mgmt_dashboard")
        with n3:
            if st.button("👥 Employees", key="ma_emp"): go_fn("mgmt_employees")
        with n4:
            if st.button("🎯 Predict", key="ma_pred"): go_fn("mgmt_predict")
        with lc:
            st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
            if st.button("Sign Out", key="ma_logout"): logout()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="page-title">Analytics & Reports</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Department-wise insights, top performers, and trend analysis</div>', unsafe_allow_html=True)

        all_emps   = get_all_employees()
        dept_stats = get_dept_stats()
        preds      = get_predictions()

        if not all_emps:
            st.info("No employee data available.")
            return

        df      = pd.DataFrame(all_emps)
        dept_df = pd.DataFrame(dept_stats) if dept_stats else pd.DataFrame()

        CHART_TEMPLATE = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="rgba(255,255,255,0.7)", family="DM Sans"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
        )

        # ── Row 1: Employees by Dept + Salary by Dept ─────────────────────────
        st.markdown('<div class="sec-title">🏢 Department Analysis</div>', unsafe_allow_html=True)
        ch1, ch2 = st.columns(2)

        with ch1:
            dept_count = df["department"].value_counts().reset_index()
            dept_count.columns = ["Department","Count"]
            fig = px.bar(dept_count, x="Department", y="Count",
                         title="Employees per Department",
                         color="Count", color_continuous_scale=["#6c63ff","#3ecfcf"])
            fig.update_layout(**CHART_TEMPLATE, title_font_size=14, showlegend=False,
                              coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        with ch2:
            if not dept_df.empty:
                fig2 = px.bar(dept_df, x="department", y="avg_salary",
                              title="Average Salary by Department",
                              color="avg_salary", color_continuous_scale=["#f59e0b","#34d399"])
                fig2.update_layout(**CHART_TEMPLATE, title_font_size=14, showlegend=False,
                                   coloraxis_showscale=False)
                st.plotly_chart(fig2, use_container_width=True)

        # ── Row 2: Satisfaction + Attendance ─────────────────────────────────
        ch3, ch4 = st.columns(2)

        with ch3:
            if not dept_df.empty:
                fig3 = px.bar(dept_df, x="department", y="avg_satisfaction",
                              title="Avg Satisfaction Score by Department",
                              color="avg_satisfaction",
                              color_continuous_scale=["#fb7185","#fbbf24","#34d399"])
                fig3.update_layout(**CHART_TEMPLATE, title_font_size=14, showlegend=False,
                                   coloraxis_showscale=False)
                st.plotly_chart(fig3, use_container_width=True)

        with ch4:
            if not dept_df.empty:
                fig4 = px.bar(dept_df, x="department", y="avg_attendance",
                              title="Avg Attendance % by Department",
                              color="avg_attendance",
                              color_continuous_scale=["#fb7185","#fbbf24","#34d399"])
                fig4.update_layout(**CHART_TEMPLATE, title_font_size=14, showlegend=False,
                                   coloraxis_showscale=False)
                st.plotly_chart(fig4, use_container_width=True)

        # ── Row 3: Gender pie + Education ────────────────────────────────────
        st.markdown('<div class="sec-title">👤 Workforce Breakdown</div>', unsafe_allow_html=True)
        ch5, ch6 = st.columns(2)

        with ch5:
            gender_counts = df["gender"].value_counts().reset_index()
            gender_counts.columns = ["Gender","Count"]
            fig5 = px.pie(gender_counts, names="Gender", values="Count",
                          title="Gender Distribution",
                          color_discrete_sequence=["#6c63ff","#3ecfcf","#f59e0b"])
            fig5.update_layout(**CHART_TEMPLATE, title_font_size=14)
            st.plotly_chart(fig5, use_container_width=True)

        with ch6:
            edu_counts = df["education_level"].value_counts().reset_index()
            edu_counts.columns = ["Education","Count"]
            fig6 = px.pie(edu_counts, names="Education", values="Count",
                          title="Education Level Distribution",
                          color_discrete_sequence=["#6c63ff","#3ecfcf","#f59e0b","#fb7185"])
            fig6.update_layout(**CHART_TEMPLATE, title_font_size=14)
            st.plotly_chart(fig6, use_container_width=True)

        # ── Performance predictions breakdown ─────────────────────────────────
        if preds:
            st.markdown('<div class="sec-title">🎯 Prediction Analytics</div>', unsafe_allow_html=True)
            pred_df = pd.DataFrame(preds)

            ch7, ch8 = st.columns(2)
            with ch7:
                cat_counts = pred_df["category"].value_counts().reset_index()
                cat_counts.columns = ["Category","Count"]
                color_map = {
                    "Excellent Performer": "#34d399",
                    "Average Performer": "#fbbf24",
                    "Below Average Performer": "#fb7185"
                }
                fig7 = px.pie(cat_counts, names="Category", values="Count",
                              title="Performance Category Distribution",
                              color="Category", color_discrete_map=color_map)
                fig7.update_layout(**CHART_TEMPLATE, title_font_size=14)
                st.plotly_chart(fig7, use_container_width=True)

            with ch8:
                if "department" in pred_df.columns:
                    dept_score = pred_df.groupby("department")["predicted_score"].mean().reset_index()
                    dept_score.columns = ["Department","Avg Score"]
                    fig8 = px.bar(dept_score, x="Department", y="Avg Score",
                                  title="Avg Predicted Score by Department",
                                  color="Avg Score",
                                  color_continuous_scale=["#fb7185","#fbbf24","#34d399"])
                    fig8.update_layout(**CHART_TEMPLATE, title_font_size=14,
                                       coloraxis_showscale=False)
                    st.plotly_chart(fig8, use_container_width=True)

        # ── Top performers ────────────────────────────────────────────────────
        st.markdown('<div class="sec-title">🏆 Top Performers</div>', unsafe_allow_html=True)

        if preds:
            pred_df = pd.DataFrame(preds)
            top = pred_df.sort_values("predicted_score", ascending=False).head(5)
            for _, row in top.iterrows():
                emp_match = next((e for e in all_emps if e["employee_id"] == row["employee_id"]), {})
                emp_name  = emp_match.get("full_name", row["employee_id"])
                dept      = row.get("department","—")
                score     = row["predicted_score"]
                cat       = row["category"]
                color     = "#34d399" if "Excellent" in cat else "#fbbf24" if "Average" in cat else "#fb7185"
                st.markdown(f"""
                <div class="info-card" style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-family:'Syne',sans-serif;font-weight:700;color:white;">{emp_name}</div>
                        <div style="font-size:0.78rem;color:rgba(255,255,255,0.35);">{dept} &nbsp;·&nbsp; {row['employee_id']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:white;">{score}</div>
                        <div style="font-size:0.75rem;color:{color};">{cat}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Run predictions first to see top performers.")

        # ── Download full report ──────────────────────────────────────────────
        st.markdown('<div class="sec-title">📥 Download Reports</div>', unsafe_allow_html=True)
        dl1, dl2 = st.columns(2)

        with dl1:
            csv_emp = df.to_csv(index=False)
            st.download_button("📋 Download Employee Data (CSV)",
                               csv_emp, "employees.csv", "text/csv",
                               use_container_width=True)
        with dl2:
            if preds:
                csv_pred = pd.DataFrame(preds).to_csv(index=False)
                st.download_button("🎯 Download Prediction Report (CSV)",
                                   csv_pred, "predictions.csv", "text/csv",
                                   use_container_width=True)
