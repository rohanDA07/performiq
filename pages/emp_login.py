import streamlit as st
from utils.styles import GLOBAL_CSS
from database import auth_employee

CSS = GLOBAL_CSS + """
<style>
.auth-header { text-align:center; margin-bottom:2.5rem; }
.auth-icon {
    width:60px; height:60px;
    background: linear-gradient(135deg, #3ecfcf, #0ea5e9);
    border-radius:16px;
    display:inline-flex; align-items:center; justify-content:center;
    font-size:1.8rem; margin-bottom:1rem;
    box-shadow: 0 8px 24px rgba(62,207,207,0.3);
}
.auth-title { font-family:'Syne',sans-serif; font-weight:800; font-size:1.7rem; color:white; }
.auth-sub   { color:rgba(255,255,255,0.35); font-size:0.85rem; margin-top:0.3rem; }
.stButton > button { width:100%; }
</style>
"""


def show(go, go_back):
    st.markdown(CSS, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.write("")
        if st.button("← Back", key="emp_back"):
            go_back()

        st.markdown("""
        <div style="padding-top:1rem;">
        <div class="auth-header">
            <div class="auth-icon">👤</div>
            <div class="auth-title">Employee Login</div>
            <div class="auth-sub">Sign in to view and update your profile</div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In", "New? Register"])

        with tab1:
            st.write("")
            username = st.text_input("Username", placeholder="Enter username", key="e_user")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="e_pass")
            st.write("")

            if st.button("Sign In →", key="emp_signin", use_container_width=True):
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    emp = auth_employee(username, password)
                    if emp:
                        st.session_state.logged_in   = True
                        st.session_state.role        = "employee"
                        st.session_state.username    = username
                        st.session_state.name        = emp["full_name"]
                        st.session_state.employee_id = emp["employee_id"]
                        go("emp_dashboard")
                    else:
                        st.error("Invalid credentials.")

            st.markdown("""
            <div style="background:rgba(62,207,207,0.07);border:1px solid rgba(62,207,207,0.2);
                        border-radius:10px;padding:0.8rem 1rem;margin-top:1.2rem;
                        font-size:0.8rem;color:rgba(255,255,255,0.4);">
                <b style="color:rgba(255,255,255,0.6);">Demo credentials</b><br>
                <code style="color:#5eeaea;">john_doe</code> / <code style="color:#5eeaea;">emp123</code>
                &nbsp;|&nbsp;
                <code style="color:#5eeaea;">jane_smith</code> / <code style="color:#5eeaea;">emp123</code>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.write("")
            if st.button("Go to Registration →", key="go_reg", use_container_width=True):
                go("emp_register")
