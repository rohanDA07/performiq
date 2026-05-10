import streamlit as st
from utils.styles import GLOBAL_CSS, topbar, perf_class, perf_emoji
from database import get_employee_by_id, save_prediction, get_predictions
from utils.predictor import predict


def show(go, go_back, logout):
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    name   = st.session_state.get("name", "Employee")
    emp_id = st.session_state.get("employee_id", "")

    st.markdown(topbar("My Performance", name, "employee"), unsafe_allow_html=True)

    pad = st.columns([0.03, 0.94, 0.03])
    with pad[1]:
        bc, _, lc = st.columns([1.5, 8, 1.5])
        with bc:
            if st.button("← Back", key="epred_back"):
                go_back()
        with lc:
            st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
            if st.button("Sign Out", key="epred_logout"):
                logout()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="page-title">My Performance Prediction</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Based on your profile data — update your profile for accurate predictions</div>', unsafe_allow_html=True)

        emp = get_employee_by_id(emp_id)

        if not emp:
            st.warning("Profile not found. Please complete your profile first.")
            if st.button("Go to Profile"):
                go("emp_profile")
            return

        # Show current profile summary
        st.markdown('<div class="sec-title">📋 Your Current Data (used for prediction)</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        cols = [c1, c2, c3, c4]
        fields = [
            ("Department", emp.get("department","—")),
            ("Designation", emp.get("designation","—")),
            ("Experience", f"{emp.get('experience','—')} yrs"),
            ("Attendance", f"{emp.get('attendance_pct','—')}%"),
            ("Projects", emp.get("projects_completed","—")),
            ("Training Hrs", emp.get("training_hours","—")),
            ("Satisfaction", emp.get("satisfaction_score","—")),
            ("Salary", f"${emp.get('salary','—'):,}" if emp.get('salary') else "—"),
        ]
        for i, (label, val) in enumerate(fields):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="info-card" style="text-align:center;padding:1rem;">
                    <div style="font-size:0.72rem;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:1px;">{label}</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;color:white;margin-top:0.3rem;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        st.write("")
        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            predict_btn = st.button("🎯  Predict My Performance Score", use_container_width=True, key="emp_predict_btn")

        if predict_btn:
            try:
                score, category, suggestions = predict(emp)
                save_prediction(emp_id, score, category, emp.get("department",""), predicted_by="self")

                pclass = perf_class(category)
                pemoji = perf_emoji(category)

                _, res_col, _ = st.columns([0.5, 2, 0.5])
                with res_col:
                    st.markdown(f"""
                    <div class="result-wrap">
                        <div style="color:rgba(255,255,255,0.4);font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;">
                            YOUR PERFORMANCE SCORE
                        </div>
                        <div class="result-score">{score}</div>
                        <div style="color:rgba(255,255,255,0.35);font-size:0.8rem;">out of 5.0</div>
                        <div style="margin-top:0.8rem;">
                            <span class="perf-badge {pclass}">{pemoji} {category}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.progress(score / 5.0)

                # Suggestions
                st.markdown('<div class="sec-title">💡 Improvement Suggestions</div>', unsafe_allow_html=True)
                for tip in suggestions:
                    st.markdown(f"""
                    <div class="info-card" style="margin-bottom:0.6rem;padding:0.9rem 1.2rem;">
                        <span style="color:rgba(255,255,255,0.8);">{tip}</span>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction error: {e}\nMake sure the model file exists at the configured path.")

        # ── Prediction history ────────────────────────────────────────────────
        records = get_predictions(emp_id)
        if records:
            st.markdown('<div class="sec-title">📅 Prediction History</div>', unsafe_allow_html=True)
            import pandas as pd
            hist_df = pd.DataFrame(records)[["predicted_at","predicted_score","category"]]
            hist_df.columns = ["Date", "Score", "Category"]
            st.dataframe(hist_df, use_container_width=True, hide_index=True)
