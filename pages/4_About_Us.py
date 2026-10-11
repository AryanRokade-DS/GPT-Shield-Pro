import streamlit as st
from utils import inject_global_css

st.set_page_config(page_title="About Us", page_icon="ℹ️", layout="wide")
inject_global_css()

st.markdown("""
<div class="dash-hero">
    <div class="dash-hero-title">About GPT Shield Pro</div>
    <div class="dash-hero-sub">
        A smart AI platform for text authenticity, plagiarism similarity, and semantic comparison.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="panel-card">', unsafe_allow_html=True)
st.subheader("Project Overview")
st.write("""
GPT Shield Pro is an intelligent platform designed to:
- detect likely AI-generated writing,
- estimate plagiarism similarity,
- compare semantic meaning using sentence embeddings,
- inspect sentence-level similarity matches,
- and present everything with colorful interactive analytics.
""")
st.markdown('</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.subheader("Technologies Used")
    st.write("""
- Streamlit  
- GPT-2 via Transformers  
- Sentence Transformers  
- Cosine Similarity  
- NLTK  
- Plotly  
- SQLite  
""")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.subheader("Why We Built This")
    st.write("""
This system was created to combine AI detection, plagiarism similarity, semantic analysis, and visual exploration into one practical product.
""")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="panel-card">', unsafe_allow_html=True)
st.subheader("Developer")
st.write("Aryan Rokade")
st.write("Data Science student building practical AI/ML products.")
st.markdown('</div>', unsafe_allow_html=True)