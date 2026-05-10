import streamlit as st
from utils.styles import GLOBAL_CSS
from database import auth_management

CSS = GLOBAL_CSS + """
<style>
.auth-wrap { min-height:100vh; display:flex; align-items:center; justify-content:center; padding:2rem; }
.auth-card {
    background: linear-gradient(145deg, #13131a, #1a1a26);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
    padding: 3rem 3.5rem;
    width: 100%; max-width: 460px;
    box-shadow: 0 40px 80px rgba(0,0,0,0.6);
}
.auth-header { text-align:center; margin-bottom:2.5rem; }
.auth-icon {
    width:60px; height:60px;
    background: linear-gradient(135deg, #6c63ff, #4f46e5);
    border-radius:16px;
    display:inline-flex; align-items:center; justify-content:center;
    font-size:1.8rem; margin-bottom:1rem;
    box-shadow: 0 8px 24px rgba(108,99,255,0.35);
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
        # Back button
        st.write("")
        if st.button("← Back", key="mgmt_back"):
            go_back()

        st.markdown("""
        <div style="padding-top:1rem;">
        <div class="auth-header">
            <div class="auth-icon">🏢</div>
            <div class="auth-title">Management Login</div>
            <div class="auth-sub">Sign in to access the management portal</div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter username", key="m_user")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="m_pass")
        st.write("")

        if st.button("Sign In →", key="mgmt_signin", use_container_width=True):
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                user = auth_management(username, password)
                if user:
                    st.session_state.logged_in  = True
                    st.session_state.role       = "management"
                    st.session_state.username   = username
                    st.session_state.name       = user["name"]
                    go("mgmt_dashboard")
                else:
                    st.error("Invalid credentials.")

        st.markdown("""
        <div style="background:rgba(108,99,255,0.08);border:1px solid rgba(108,99,255,0.2);
                    border-radius:10px;padding:0.8rem 1rem;margin-top:1.2rem;
                    font-size:0.8rem;color:rgba(255,255,255,0.4);">
            <b style="color:rgba(255,255,255,0.6);">Demo credentials</b><br>
            Username: <code style="background:rgba(108,99,255,0.2);padding:0 4px;border-radius:4px;color:#a89fff;">admin</code>
            &nbsp; Password: <code style="background:rgba(108,99,255,0.2);padding:0 4px;border-radius:4px;color:#a89fff;">admin123</code>
        </div>
        """, unsafe_allow_html=True)
