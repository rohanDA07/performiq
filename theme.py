"""
theme.py — Shared CSS, colors, and icons for PerformIQ
"""

DEPT_ICONS = {
    "IT": "💻", "Finance": "💰", "Engineering": "⚙️", "HR": "🧑‍💼",
    "Sales": "📈", "Marketing": "📣", "Operations": "🔧",
    "Legal": "⚖️", "Customer Support": "🎧", "All": "🌐"
}

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg:        #08080f;
    --bg2:       #0f0f1a;
    --bg3:       #14141f;
    --border:    rgba(255,255,255,0.07);
    --border2:   rgba(255,255,255,0.12);
    --text:      #f0f0f8;
    --text2:     rgba(240,240,248,0.55);
    --text3:     rgba(240,240,248,0.3);
    --accent:    #7c6aff;
    --accent2:   #2ee8c8;
    --amber:     #f5a623;
    --rose:      #f43f5e;
    --emerald:   #10b981;
    --radius:    14px;
    --radius-lg: 20px;
}

* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }

.stApp {
    background: var(--bg) !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text);
}

/* Hide streamlit chrome */
header[data-testid="stHeader"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { background: var(--bg2) !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    padding: 0.6rem 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,106,255,0.15) !important;
}
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stSlider label, .stRadio label {
    color: var(--text2) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}
.stSelectbox > div > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--accent) !important;
}

/* Primary button */
.stButton > button[kind="primary"],
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Clash Display', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    letter-spacing: 0.2px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Secondary button */
.stButton > button[kind="secondary"] {
    background: var(--bg3) !important;
    color: var(--text2) !important;
    border: 1px solid var(--border2) !important;
}

/* Danger button */
.danger-btn > button {
    background: rgba(244,63,94,0.12) !important;
    color: #fb7185 !important;
    border: 1px solid rgba(244,63,94,0.25) !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
}

/* Alerts */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* Tabs */
[data-testid="stTabs"] button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
    color: var(--text2) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--text) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] iframe { border-radius: 12px !important; }

/* Divider */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* Metric */
[data-testid="stMetric"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text2) !important; font-size: 0.78rem !important; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-family: 'Clash Display', sans-serif !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: rgba(124,106,255,0.3); border-radius: 10px; }
</style>
"""

TOPBAR_CSS = """
<style>
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2.5rem;
    background: rgba(15,15,26,0.95);
    border-bottom: 1px solid var(--border);
    position: sticky; top: 0; z-index: 100;
    backdrop-filter: blur(12px);
}
.topbar-brand {
    font-family: 'Clash Display', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.topbar-brand .accent {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.topbar-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.user-pill {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: var(--bg3);
    border: 1px solid var(--border2);
    border-radius: 50px;
    padding: 0.35rem 1rem 0.35rem 0.4rem;
}
.avatar {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    color: white;
}
.user-name { font-size: 0.82rem; color: var(--text2); font-weight: 500; }
.role-chip {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
}
.role-chip.mgmt { background: rgba(124,106,255,0.15); color: #a89fff; border: 1px solid rgba(124,106,255,0.25); }
.role-chip.emp  { background: rgba(46,232,200,0.12);  color: #2ee8c8; border: 1px solid rgba(46,232,200,0.2); }
</style>
"""

CARD_CSS = """
<style>
.stat-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin: 1.5rem 0; }
.stat-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: var(--border2); }
.stat-card .accent-line {
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
}
.stat-label { font-size: 0.72rem; color: var(--text3); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }
.stat-val   { font-family: 'Clash Display', sans-serif; font-size: 1.8rem; font-weight: 700; color: var(--text); line-height: 1; }
.stat-sub   { font-size: 0.75rem; color: var(--text3); margin-top: 0.3rem; }

.dept-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px,1fr)); gap: 0.8rem; margin: 1rem 0 1.5rem 0; }
.dept-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    text-align: center;
    transition: all 0.2s;
    cursor: pointer;
}
.dept-card:hover { border-color: var(--border2); background: var(--bg3); transform: translateY(-1px); }
.dept-card.active { border-color: var(--accent); background: rgba(124,106,255,0.1); }
.dept-icon { font-size: 1.5rem; margin-bottom: 0.4rem; }
.dept-name { font-family: 'Clash Display', sans-serif; font-size: 0.82rem; font-weight: 600; color: var(--text); }
.dept-count { font-size: 0.72rem; color: var(--text3); margin-top: 0.15rem; }

.section-head {
    font-family: 'Clash Display', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text);
    margin: 2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-head::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
    margin-left: 0.8rem;
}

.perf-result {
    background: linear-gradient(135deg, var(--bg2), var(--bg3));
    border: 1px solid var(--border2);
    border-radius: var(--radius-lg);
    padding: 2.5rem 2rem;
    text-align: center;
    margin-top: 1.5rem;
}
.perf-score {
    font-family: 'Clash Display', sans-serif;
    font-size: 4.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.perf-score-label { font-size: 0.78rem; color: var(--text3); margin-bottom: 0.3rem; }
.perf-badge-wrap  { margin: 1rem 0 0.8rem 0; }
.perf-badge {
    display: inline-block;
    padding: 0.5rem 1.8rem;
    border-radius: 50px;
    font-family: 'Clash Display', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.3px;
}
.badge-excellent { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.badge-average   { background: rgba(245,166,35,0.15);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.badge-below     { background: rgba(244,63,94,0.15);   color: #fb7185; border: 1px solid rgba(251,113,133,0.3); }
.perf-suggestion { font-size: 0.86rem; color: var(--text2); margin-top: 0.6rem; max-width: 380px; margin-left: auto; margin-right: auto; line-height: 1.65; }
</style>
"""


def topbar_html(name: str, role: str, emp_id: str = "") -> str:
    initials = "".join([w[0].upper() for w in name.split()[:2]])
    role_label = "Management" if role == "management" else "Employee"
    chip_class = "mgmt" if role == "management" else "emp"
    sub = emp_id if role == "employee" else "Admin"
    return f"""
    <div class="topbar">
        <div class="topbar-brand">
            <span style="font-size:1.3rem;">📊</span>
            Perform<span class="accent">IQ</span>
        </div>
        <div class="topbar-right">
            <div class="user-pill">
                <div class="avatar">{initials}</div>
                <span class="user-name">{name}</span>
            </div>
            <span class="role-chip {chip_class}">{role_label}</span>
        </div>
    </div>
    """


def perf_category(score: float):
    if score >= 4.0:
        return "Excellent Performer", "badge-excellent", "🚀", \
               "Outstanding results! Recommend for leadership opportunities, performance bonus, and recognition programs."
    elif score >= 2.5:
        return "Average Performer", "badge-average", "👍", \
               "Solid contributor. Consider targeted skill development, mentoring, and clearer KPI alignment."
    else:
        return "Below Average Performer", "badge-below", "⚠️", \
               "Performance needs improvement. Recommend a structured PIP, additional training, and regular 1:1 check-ins."


def inject_css(*extra):
    import streamlit as st
    combined = GLOBAL_CSS + TOPBAR_CSS + CARD_CSS + "".join(extra)
    st.markdown(combined, unsafe_allow_html=True)
