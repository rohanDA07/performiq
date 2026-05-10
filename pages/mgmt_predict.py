import streamlit as st
import pandas as pd
import io
from utils.styles import GLOBAL_CSS, topbar, perf_class, perf_emoji
from database import get_all_employees, save_prediction, get_predictions
from utils.predictor import predict

DEPTS = ["IT","Finance","Engineering","HR","Sales","Marketing","Operations","Legal","Customer Support"]
JOBS  = ["Analyst","Developer","Specialist","Engineer","Manager","Consultant","Technician","Intern"]
EDUS  = ["High School","Bachelor","Master","PhD"]

def _idx(lst, val):
    try: return lst.index(val)
    except: return 0


def show(go, go_back, logout):
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

    name = st.session_state.get("name","Manager")
    st.markdown(topbar("Predict Performance", name, "management"), unsafe_allow_html=True)

    pad = st.columns([0.03, 0.94, 0.03])
    with pad[1]:
        n1, n2, n3, n4, _, lc = st.columns([1.5, 1.8, 1.8, 2, 3, 1.5])
        with n1:
            if st.button("← Back", key="mp_back"): go_back()
        with n2:
            if st.button("🏠 Dashboard", key="mp_dash"): go("mgmt_dashboard")
        with n3:
            if st.button("👥 Employees", key="mp_emp"): go("mgmt_employees")
        with n4:
            if st.button("📊 Analytics", key="mp_ana"): go("mgmt_analytics")
        with lc:
            st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
            if st.button("Sign Out", key="mp_logout"): logout()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="page-title">Performance Prediction</div>', unsafe_allow_html=True)
        st.markdown('<div class="page-sub">Use the ML model to predict and categorize employee performance</div>', unsafe_allow_html=True)

        all_emps = get_all_employees()
        mode = st.radio("Mode", ["Pick existing employee", "Enter manually"], horizontal=True, key="pred_mode")

        emp_data = {}
        if mode == "Pick existing employee" and all_emps:
            options = {f"{e['full_name']} ({e['employee_id']}) — {e.get('department','')}": e for e in all_emps}
            chosen  = st.selectbox("Select Employee", list(options.keys()))
            emp_data = options[chosen]
            st.info(f"Loaded data for **{emp_data.get('full_name','')}**. Adjust below if needed.")

        st.markdown('<div class="sec-title">📋 Prediction Inputs</div>', unsafe_allow_html=True)
        with st.form("predict_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                department  = st.selectbox("Department", DEPTS, index=_idx(DEPTS, emp_data.get("department","IT")))
                gender      = st.selectbox("Gender", ["Male","Female","Other"], index=_idx(["Male","Female","Other"], emp_data.get("gender","Male")))
                designation = st.selectbox("Designation", JOBS, index=_idx(JOBS, emp_data.get("designation","Analyst")))
                education   = st.selectbox("Education", EDUS, index=_idx(EDUS, emp_data.get("education_level","Bachelor")))
            with c2:
                age         = st.number_input("Age", 18, 65, int(emp_data.get("age") or 30))
                experience  = st.number_input("Experience (yrs)", 0, 40, int(emp_data.get("experience") or 5))
                salary      = st.number_input("Monthly Salary", 3000, 100000, int(emp_data.get("salary") or 6000), step=500)
                working_hours = st.number_input("Working Hrs/Week", 20.0, 80.0, float(emp_data.get("working_hours") or 40.0))
            with c3:
                projects_completed  = st.number_input("Projects Completed", 0, 500, int(emp_data.get("projects_completed") or 10))
                overtime_hours      = st.number_input("Overtime Hrs", 0.0, 100.0, float(emp_data.get("overtime_hours") or 5.0))
                training_hours      = st.number_input("Training Hrs", 0.0, 500.0, float(emp_data.get("training_hours") or 20.0))
                promotions          = st.number_input("Promotions", 0, 10, int(emp_data.get("promotions") or 0))
                satisfaction_score  = st.slider("Satisfaction Score", 1.0, 5.0, float(emp_data.get("satisfaction_score") or 3.0), 0.1)

            predict_btn = st.form_submit_button("🎯  Predict Performance Score", use_container_width=True)

        if predict_btn:
            input_data = {
                "department": department, "gender": gender, "designation": designation,
                "education_level": education, "age": age, "experience": experience,
                "salary": salary, "working_hours": working_hours,
                "projects_completed": projects_completed, "overtime_hours": overtime_hours,
                "training_hours": training_hours, "promotions": promotions,
                "satisfaction_score": satisfaction_score,
            }
            try:
                score, category, suggestions = predict(input_data)
                emp_id_used = emp_data.get("employee_id","manual")
                save_prediction(emp_id_used, score, category, department, predicted_by=name)

                pclass = perf_class(category)
                pemoji = perf_emoji(category)

                _, res_col, _ = st.columns([0.5, 2, 0.5])
                with res_col:
                    st.markdown(f"""
                    <div class="result-wrap">
                        <div style="color:rgba(255,255,255,0.4);font-size:0.8rem;letter-spacing:1px;text-transform:uppercase;">
                            PREDICTED PERFORMANCE SCORE
                        </div>
                        <div class="result-score">{score}</div>
                        <div style="color:rgba(255,255,255,0.35);font-size:0.82rem;">out of 5.0</div>
                        <span class="perf-badge {pclass}">{pemoji} {category}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(score / 5.0)

                st.markdown('<div class="sec-title">💡 Recommendations</div>', unsafe_allow_html=True)
                for tip in suggestions:
                    st.markdown(f'<div class="info-card" style="padding:0.8rem 1.2rem;">{tip}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction failed: {e}\nEnsure the model file exists.")

        # ── Bulk predict ──────────────────────────────────────────────────────
        st.markdown('<div class="sec-title">⚡ Bulk Predict All Employees</div>', unsafe_allow_html=True)

        if st.button("🚀 Run Bulk Prediction on All Employees", use_container_width=True, key="bulk_pred"):
            results = []
            errors  = 0
            progress = st.progress(0)
            for i, emp in enumerate(all_emps):
                try:
                    score, category, _ = predict(emp)
                    save_prediction(emp["employee_id"], score, category, emp.get("department",""), predicted_by=name)
                    results.append({
                        "Employee ID": emp["employee_id"],
                        "Name": emp.get("full_name",""),
                        "Department": emp.get("department",""),
                        "Score": score,
                        "Category": category,
                    })
                except:
                    errors += 1
                progress.progress((i+1)/len(all_emps))

            if results:
                st.success(f"✅ Predicted {len(results)} employees." + (f" ({errors} errors)" if errors else ""))
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Download
                csv = df.to_csv(index=False)
                st.download_button("📥 Download Report (CSV)", csv,
                                   file_name="performance_report.csv", mime="text/csv",
                                   use_container_width=True)
