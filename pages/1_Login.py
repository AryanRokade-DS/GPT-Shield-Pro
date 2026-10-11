import streamlit as st
from auth import init_db, login_user
from utils import inject_global_css

st.set_page_config(page_title="Login", layout="wide")
inject_global_css()
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

left, center, right = st.columns([1, 1.15, 1])

with center:
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-icon">🔒</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Welcome back</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">Sign in to your account to continue</div>', unsafe_allow_html=True)

    st.markdown('<div class="field-label">Username</div>', unsafe_allow_html=True)
    username = st.text_input("Username", label_visibility="collapsed", placeholder="Enter your username")

    st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
    password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter your password")

    c1, c2 = st.columns([1, 1])
    with c1:
        remember_me = st.checkbox("Remember me")
    with c2:
        st.markdown('<div style="text-align:right; padding-top:8px; color:#374151; font-size:14px;">Forgot password?</div>', unsafe_allow_html=True)

    if st.button("Sign in", use_container_width=True):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = {
                "id": user[0],
                "name": user[1],
                "username": user[2],
                "email": user[3]
            }
            st.success("Login successful")
            st.switch_page("pages/3_Dashboard.py")
        else:
            st.error("Invalid credentials")

    st.markdown("""
    <div class="divider-wrap">
        <div class="divider-line"></div>
        <div>Or continue with</div>
        <div class="divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="social-grid">
        <div class="social-box">Google</div>
        <div class="social-box">GitHub</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bottom-note">
        Don’t have an account? <a href="/Register" target="_self">Sign up</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)