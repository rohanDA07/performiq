import streamlit as st
from utils.styles import GLOBAL_CSS

CSS = GLOBAL_CSS + """
<style>
.login-page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem;
    background: radial-gradient(ellipse at 30% 20%, rgba(108,99,255,0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 80%, rgba(62,207,207,0.06) 0%, transparent 60%);
}
.brand-wrap { text-align: center; margin-bottom: 3rem; }
.brand-logo {
    width: 72px; height: 72px;
    background: linear-gradient(135deg, #6c63ff, #3ecfcf);
    border-radius: 20px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 2.2rem; margin-bottom: 1rem;
    box-shadow: 0 12px 40px rgba(108,99,255,0.4);
}
.brand-name {
    font-family: 'Syne', sans-serif;
    font-weight: 800; font-size: 2.8rem;
    color: white; letter-spacing: -1.5px;
}
.brand-name span {
    background: linear-gradient(135deg, #6c63ff, #3ecfcf);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.brand-tagline { color: rgba(255,255,255,0.35); font-size: 1rem; margin-top: 0.5rem; }

.choose-label {
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 0.88rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

.role-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; width: 100%; max-width: 560px; }

.role-card {
    background: rgba(255,255,255,0.03);
    border: 1.5px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 2.5rem 2rem;
    text-align: center;
    transition: all 0.25s;
    position: relative;
    overflow: hidden;
}
.role-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(108,99,255,0.08), transparent);
    opacity: 0;
    transition: opacity 0.25s;
}
.role-card:hover::before { opacity: 1; }
.role-card:hover { border-color: rgba(108,99,255,0.4); transform: translateY(-3px); box-shadow: 0 16px 40px rgba(0,0,0,0.4); }

.role-icon-wrap {
    width: 64px; height: 64px;
    border-radius: 18px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 2rem; margin-bottom: 1.2rem;
}
.role-icon-mgmt { background: linear-gradient(135deg, rgba(108,99,255,0.25), rgba(108,99,255,0.1)); border: 1px solid rgba(108,99,255,0.3); }
.role-icon-emp  { background: linear-gradient(135deg, rgba(62,207,207,0.25), rgba(62,207,207,0.1));  border: 1px solid rgba(62,207,207,0.3);  }

.role-title { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.2rem; color: white; margin-bottom: 0.4rem; }
.role-desc  { font-size: 0.8rem; color: rgba(255,255,255,0.35); line-height: 1.5; }

.stButton > button { width: 100%; margin-top: 1.2rem !important; }
</style>
"""


def show(go):
    st.markdown(CSS, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.6, 1])
    with mid:
        st.markdown("""
        <div style="text-align:center; padding: 4rem 0 0 0;">
            <div class="brand-logo">📊</div>
            <div class="brand-name">Perform<span>IQ</span></div>
            <div class="brand-tagline">Employee Intelligence & Performance Platform</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="choose-label">Select your role to continue</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("""
            <div class="role-card">
                <div class="role-icon-wrap role-icon-mgmt">🏢</div>
                <div class="role-title">Management</div>
                <div class="role-desc">Access all employee records, analytics, and performance predictions</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Management Login →", key="go_mgmt", use_container_width=True):
                go("mgmt_login")

        with c2:
            st.markdown("""
            <div class="role-card">
                <div class="role-icon-wrap role-icon-emp">👤</div>
                <div class="role-title">Employee</div>
                <div class="role-desc">View your profile, update details, and check your performance score</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Employee Login →", key="go_emp", use_container_width=True):
                go("emp_login")

        st.write("")
        st.markdown("""
        <div style="text-align:center;font-size:0.75rem;color:rgba(255,255,255,0.2);margin-top:1rem;padding-bottom:3rem;">
            Demo: Management → admin / admin123 &nbsp;|&nbsp; Employee → john_doe / emp123
        </div>
        """, unsafe_allow_html=True)
