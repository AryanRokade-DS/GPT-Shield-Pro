import streamlit as st
from auth import init_db, register_user
from utils import inject_global_css

st.set_page_config(page_title="Register", layout="wide")
inject_global_css()
init_db()

left, center, right = st.columns([1, 1.2, 1])

with center:
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-icon">📝</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Create account</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">Create your profile and start using GPT Shield Pro</div>', unsafe_allow_html=True)

    st.markdown('<div class="field-label">Full Name</div>', unsafe_allow_html=True)
    name = st.text_input("Full Name", label_visibility="collapsed", placeholder="Enter your full name")

    st.markdown('<div class="field-label">Username</div>', unsafe_allow_html=True)
    username = st.text_input("Username", label_visibility="collapsed", placeholder="Choose a username")

    st.markdown('<div class="field-label">Email</div>', unsafe_allow_html=True)
    email = st.text_input("Email", label_visibility="collapsed", placeholder="Enter your email")

    st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
    password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Create a password")

    st.markdown('<div class="field-label">Confirm Password</div>', unsafe_allow_html=True)
    confirm = st.text_input("Confirm Password", type="password", label_visibility="collapsed", placeholder="Confirm your password")

    if st.button("Register", use_container_width=True):
        if not all([name, username, email, password, confirm]):
            st.warning("Please fill all fields.")
        elif password != confirm:
            st.error("Passwords do not match")
        else:
            ok, msg = register_user(name, username, email, password)
            if ok:
                st.success(msg)
                st.switch_page("pages/1_Login.py")
            else:
                st.error(msg)

    st.markdown("""
    <div class="bottom-note">
        Already have an account? <a href="/Login" target="_self">Sign in</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)