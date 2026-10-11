import streamlit as st
from utils import inject_global_css

st.set_page_config(
    page_title="GPT Shield Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_global_css()

st.markdown("""
<div class="page-hero">
    <div class="page-hero-title">GPT Shield Pro</div>
    <div class="page-hero-sub">
        A smart AI platform for plagiarism similarity, semantic sentence matching,
        interactive analytics, and intelligent text authenticity analysis.
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="ui-stat blue">
        <div class="ui-stat-label">AI Detection</div>
        <div class="ui-stat-value">Enabled</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="ui-stat purple">
        <div class="ui-stat-label">Plagiarism Check</div>
        <div class="ui-stat-value">Semantic Similarity</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="ui-stat pink">
        <div class="ui-stat-label">System Status</div>
        <div class="ui-stat-value">Ready</div>
    </div>
    """, unsafe_allow_html=True)

st.info("Use the sidebar to open Login, Register, Dashboard, and About Us.")