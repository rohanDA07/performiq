import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db


st.set_page_config(
    page_title="PerformIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Init DB on every startup
init_db()

# ── Session defaults ──────────────────────────────────────────────────────────
defaults = {
    "logged_in": False,
    "role": None,
    "user_id": None,
    "username": None,
    "name": None,
    "employee_id": None,
    "page": "login",          # current page
    "prev_page": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def go(page):
    st.session_state.prev_page = st.session_state.page
    st.session_state.page = page
    st.rerun()


def go_back():
    if st.session_state.prev_page:
        p = st.session_state.prev_page
        st.session_state.prev_page = st.session_state.page
        st.session_state.page = p
        st.rerun()


def logout():
    for k in defaults:
        st.session_state[k] = defaults[k]
    st.session_state.page = "login"
    st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "login":
    from pages.login import show
    show(go)

elif page == "emp_login":
    from pages.emp_login import show
    show(go, go_back)

elif page == "mgmt_login":
    from pages.mgmt_login import show
    show(go, go_back)

elif page == "emp_register":
    from pages.emp_register import show
    show(go, go_back)

elif page == "emp_dashboard":
    from pages.emp_dashboard import show
    show(go, go_back, logout)

elif page == "emp_profile":
    from pages.emp_profile import show
    show(go, go_back, logout)

elif page == "emp_predict":
    from pages.emp_predict import show
    show(go, go_back, logout)

elif page == "mgmt_dashboard":
    from pages.mgmt_dashboard import show
    show(go, go_back, logout)

elif page == "mgmt_employees":
    from pages.mgmt_employees import show
    show(go, go_back, logout)

elif page == "mgmt_predict":
    from pages.mgmt_predict import show
    show(go, go_back, logout)

elif page == "mgmt_analytics":
    from pages.mgmt_analytics import show
    show(go, go_back, logout)

else:
    st.session_state.page = "login"
    st.rerun()
