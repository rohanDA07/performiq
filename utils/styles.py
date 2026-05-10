GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

* { box-sizing: border-box; }

.stApp {
    background: #07070f;
    font-family: 'DM Sans', sans-serif;
    color: #e0e0e0;
}

/* Hide default streamlit chrome */
header { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { background: #0d0d18 !important; border-right: 1px solid rgba(255,255,255,0.06); }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.8) !important; }

/* Topbar */
.topbar {
    padding: 1rem 2.5rem;
    background: rgba(255,255,255,0.02);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.4rem;
    color: white;
}
.brand span {
    background: linear-gradient(135deg, #6c63ff, #3ecfcf);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.role-badge {
    padding: 0.25rem 0.85rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.badge-mgmt { background: rgba(108,99,255,0.15); border: 1px solid rgba(108,99,255,0.3); color: #a89fff; }
.badge-emp  { background: rgba(62,207,207,0.12); border: 1px solid rgba(62,207,207,0.3);  color: #5eeaea; }

/* Page title */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: white;
    margin: 1.5rem 0 0.3rem 0;
}
.page-sub { color: rgba(255,255,255,0.4); font-size: 0.88rem; margin-bottom: 1.5rem; }

/* Stat cards */
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.8rem; }
.stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.stat-card.purple::before { background: linear-gradient(90deg, #6c63ff, #9c8fff); }
.stat-card.teal::before   { background: linear-gradient(90deg, #3ecfcf, #6ef0e0); }
.stat-card.amber::before  { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.stat-card.rose::before   { background: linear-gradient(90deg, #f43f5e, #fb7185); }
.stat-card.green::before  { background: linear-gradient(90deg, #10b981, #34d399); }
.stat-label { font-size: 0.72rem; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.4rem; }
.stat-value { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; color: white; }
.stat-sub   { font-size: 0.73rem; color: rgba(255,255,255,0.3); margin-top: 0.2rem; }

/* Section title */
.sec-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: white;
    margin: 1.6rem 0 0.9rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Cards */
.info-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}

/* Performance result */
.result-wrap {
    background: linear-gradient(135deg, #0d1f3c, #0a2a2a);
    border: 1px solid rgba(62,207,207,0.15);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin: 1.5rem 0;
}
.result-score {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6c63ff, #3ecfcf);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin: 0.5rem 0;
}
.perf-badge {
    display: inline-block;
    padding: 0.5rem 1.8rem;
    border-radius: 50px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    margin-top: 0.8rem;
}
.perf-excellent { background: rgba(16,185,129,0.15);  color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.perf-average   { background: rgba(245,158,11,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.perf-below     { background: rgba(244,63,94,0.15);   color: #fb7185; border: 1px solid rgba(251,113,133,0.3); }

/* Form styling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: white !important;
}
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: white !important;
}
label, .stSelectbox label, .stTextInput label,
.stNumberInput label, .stSlider label, .stTextArea label {
    color: rgba(255,255,255,0.55) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #3ecfcf) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.4rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Back button override */
div[data-testid="stButton"]:has(button[kind="secondary"]) button {
    background: rgba(255,255,255,0.07) !important;
    color: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* Danger button */
.danger-btn > button {
    background: rgba(244,63,94,0.15) !important;
    color: #fb7185 !important;
    border: 1px solid rgba(244,63,94,0.3) !important;
}

/* Alerts */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* DataFrame */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
.dataframe { background: rgba(255,255,255,0.02) !important; }

/* Tab styling */
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.03); border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; color: rgba(255,255,255,0.5); }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #6c63ff, #3ecfcf); color: white !important; }
</style>
"""


def topbar(title, name, role):
    badge_cls = "badge-mgmt" if role == "management" else "badge-emp"
    badge_txt = "Management" if role == "management" else "Employee"
    return f"""
    <div class="topbar">
        <div class="brand">Perform<span>IQ</span> <span style="font-size:0.8rem;color:rgba(255,255,255,0.3);font-weight:400;">/ {title}</span></div>
        <div style="display:flex;align-items:center;gap:1rem;">
            <span class="role-badge {badge_cls}">{badge_txt}</span>
            <span style="color:rgba(255,255,255,0.45);font-size:0.85rem;">👤 {name}</span>
        </div>
    </div>
    """


def perf_class(category):
    if "Excellent" in category:
        return "perf-excellent"
    elif "Average" in category:
        return "perf-average"
    return "perf-below"


def perf_emoji(category):
    if "Excellent" in category: return "🏆"
    elif "Average" in category: return "👍"
    return "⚠️"
