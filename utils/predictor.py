import joblib
import pandas as pd
import os

MODEL_PATH = "Model/employee_model.pkl"

_model = None


def load_model():
    global _model

    if _model is None:

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at: {MODEL_PATH}"
            )

        _model = joblib.load(MODEL_PATH)

    return _model


def predict(employee_data: dict) -> tuple:
    """
    Returns:
    (score, category, suggestions)
    """

    model = load_model()

    input_df = pd.DataFrame([{
        "Department": employee_data.get("department", "IT"),
        "Gender": employee_data.get("gender", "Male"),
        "Job_Title": employee_data.get("designation", "Analyst"),
        "Education_Level": employee_data.get("education_level", "Bachelor"),

        "Age": employee_data.get("age", 30),
        "Years_At_Company": employee_data.get("experience", 5),

        "Monthly_Salary": employee_data.get("salary", 6000),

        "Work_Hours_Per_Week": employee_data.get("working_hours", 40),

        "Projects_Handled": employee_data.get("projects_completed", 10),

        "Overtime_Hours": employee_data.get("overtime_hours", 5),

        "Training_Hours": employee_data.get("training_hours", 20),

        "Promotions": employee_data.get("promotions", 0),

        "Employee_Satisfaction_Score":
            employee_data.get("satisfaction_score", 3.0),

        # ===== Missing columns added =====

        "Team_Size": employee_data.get("team_size", 5),

        "Remote_Work_Frequency": employee_data.get("remote_work_frequency",5),

        "Sick_Days": employee_data.get("sick_days", 2),

        "Resigned": employee_data.get("resigned", "0"),
    }])

    # Predict score
    prediction = model.predict(input_df)[0]
    score = round(float(prediction), 2)

    # Classify
    category = classify(score)

    # Suggestions
    suggestions = get_suggestion(score, employee_data)

    return score, category, suggestions


def classify(score: float) -> str:

    if score >= 4.0:
        return "Excellent Performer"

    elif score >= 3.0:
        return "Average Performer"

    else:
        return "Below Average Performer"


def get_suggestion(score: float, data: dict) -> list:

    tips = []

    if score < 3.0:

        tips.append(
            "📚 Enroll in targeted skill-development training programs."
        )

        tips.append(
            "🎯 Set clear, measurable short-term goals with your manager."
        )

        if data.get("attendance_pct", 100) < 85:
            tips.append(
                "📅 Improve attendance — aim for at least 90%."
            )

        if data.get("training_hours", 0) < 20:
            tips.append(
                "🕐 Increase training hours to build technical competency."
            )

        tips.append(
            "💬 Schedule regular 1-on-1 check-ins with your manager."
        )

    elif score < 4.0:

        tips.append(
            "🚀 Take on more challenging projects to accelerate growth."
        )

        tips.append(
            "🤝 Collaborate cross-functionally to broaden your impact."
        )

        if data.get("promotions", 0) == 0:
            tips.append(
                "⭐ Discuss a promotion roadmap with your manager."
            )

        tips.append(
            "📈 Upskill in emerging technologies relevant to your role."
        )

    else:

        tips.append(
            "🏆 You are a top performer — consider mentoring junior colleagues."
        )

        tips.append(
            "🌟 Explore leadership opportunities within your department."
        )

        tips.append(
            "💡 Share your expertise through internal workshops or presentations."
        )

        tips.append(
            "🎖️ You may be eligible for a performance bonus — speak to HR."
        )

    return tips