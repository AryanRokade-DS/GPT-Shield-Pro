import pandas as pd
import streamlit as st

from utils import (
    inject_global_css,
    detect_ai,
    semantic_similarity_score,
    plagiarism_result,
    sentence_level_matches,
    highlighted_matches_html,
    plot_top_words,
    plot_metrics,
    plot_ai_pie_chart,
    plot_sentence_similarity_distribution,
    plot_plagiarism_gauge
)

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
inject_global_css()

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first from the Login page.")
    st.stop()

user = st.session_state.get("current_user", {})
name = user.get("name", "User")

with st.sidebar:
    st.markdown("## 🛡 GPT Shield Pro")
    st.caption("AI-powered text authenticity workspace")
    st.markdown("---")
    st.write(f"Welcome, **{name}**")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.success("Logged out successfully.")

st.markdown("""
<div class="page-hero">
    <div class="page-hero-title">GPT Shield Pro Dashboard</div>
    <div class="page-hero-sub">
        Upload or paste text, compare it against references, and explore AI detection,
        plagiarism similarity, semantic sentence matching, and visual analytics.
    </div>
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
    <div class="ui-stat blue">
        <div class="ui-stat-label">Detection Engine</div>
        <div class="ui-stat-value">GPT-2 + Hybrid Metrics</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="ui-stat purple">
        <div class="ui-stat-label">Similarity Engine</div>
        <div class="ui-stat-value">Sentence Embeddings + Cosine</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="ui-stat pink">
        <div class="ui-stat-label">Visualization</div>
        <div class="ui-stat-value">Charts + Highlighted Matches</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.subheader("Input Text")
    uploaded_input = st.file_uploader("Upload input text file (.txt)", type=["txt"], key="input_file")
    input_text = ""
    if uploaded_input is not None:
        input_text = uploaded_input.read().decode("utf-8", errors="ignore")

    input_text = st.text_area(
        "Enter text to analyze",
        value=input_text,
        height=260,
        placeholder="Paste or upload the text you want to analyze..."
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.subheader("Reference Text")
    uploaded_ref = st.file_uploader("Upload reference text file (.txt)", type=["txt"], key="ref_file")
    reference_text = ""
    if uploaded_ref is not None:
        reference_text = uploaded_ref.read().decode("utf-8", errors="ignore")

    reference_text = st.text_area(
        "Enter reference/original text",
        value=reference_text,
        height=260,
        placeholder="Paste or upload source/reference text for plagiarism comparison..."
    )
    st.markdown('</div>', unsafe_allow_html=True)

analyze_clicked = st.button("Analyze", use_container_width=True)

if analyze_clicked:
    if not input_text.strip():
        st.warning("Please enter the main text.")
    elif len(input_text.split()) < 20:
        st.warning("Please enter at least 20 words for better accuracy.")
    else:
        ai_result = detect_ai(input_text)

        plagiarism_percent = None
        plagiarism_label = "Reference text not provided"
        sentence_df = pd.DataFrame()

        if reference_text.strip():
            sim_score = semantic_similarity_score(input_text, reference_text)
            plagiarism_percent, plagiarism_label = plagiarism_result(sim_score)
            sentence_df = sentence_level_matches(input_text, reference_text)

        tab1, tab2, tab3, tab4 = st.tabs([
            "Overview",
            "AI Detection",
            "Plagiarism Check",
            "Highlighted Matches"
        ])

        with tab1:
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown('<div class="metric-shell">', unsafe_allow_html=True)
                st.metric("AI Score", f'{ai_result["AI Score"]}%')
                st.progress(min(int(ai_result["AI Score"]), 100))
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                sim_val = plagiarism_percent if plagiarism_percent is not None else 0
                st.markdown('<div class="metric-shell">', unsafe_allow_html=True)
                st.metric("Similarity Score", f"{sim_val}%")
                st.progress(min(int(sim_val), 100))
                st.markdown('</div>', unsafe_allow_html=True)

            with c3:
                st.markdown('<div class="metric-shell">', unsafe_allow_html=True)
                if ai_result["Result"] == "Likely AI-generated":
                    st.markdown(f'<div class="bad-box">{ai_result["Result"]}</div>', unsafe_allow_html=True)
                elif ai_result["Result"] == "Possibly AI-generated":
                    st.markdown(f'<div class="warn-box">{ai_result["Result"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="good-box">{ai_result["Result"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            g1, g2 = st.columns(2)

            with g1:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                plot_ai_pie_chart(ai_result["AI Score"])
                st.markdown('</div>', unsafe_allow_html=True)

            with g2:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                plot_plagiarism_gauge(plagiarism_percent if plagiarism_percent is not None else 0)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            plot_top_words(input_text)
            st.markdown('</div>', unsafe_allow_html=True)

            if plagiarism_percent is not None:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                plot_metrics(ai_result, plagiarism_percent)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                plot_sentence_similarity_distribution(sentence_df)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            x, y = st.columns(2)

            with x:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                st.subheader("AI Detection Result")

                if ai_result["Result"] == "Likely AI-generated":
                    st.error(ai_result["Result"])
                elif ai_result["Result"] == "Possibly AI-generated":
                    st.warning(ai_result["Result"])
                else:
                    st.success(ai_result["Result"])

                st.metric("AI Score", f'{ai_result["AI Score"]}%')
                st.metric("Perplexity", ai_result["Perplexity"])
                st.metric("Burstiness", ai_result["Burstiness"])
                st.metric("Lexical Diversity", ai_result["Lexical Diversity"])
                st.markdown('</div>', unsafe_allow_html=True)

            with y:
                st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                st.subheader("Detailed Metrics")
                st.metric("Repetition Ratio", ai_result["Repetition Ratio"])
                st.metric("Average Sentence Length", ai_result["Average Sentence Length"])
                st.metric("Sentence Variation", ai_result["Sentence Variation"])
                st.info("This is a support tool. Use manual review for final judgment.")
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            if reference_text.strip():
                p1, p2 = st.columns([1, 1])

                with p1:
                    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                    st.subheader("Similarity Result")

                    if plagiarism_percent >= 85:
                        st.error(plagiarism_label)
                    elif plagiarism_percent >= 60:
                        st.warning(plagiarism_label)
                    else:
                        st.success(plagiarism_label)

                    st.metric("Similarity Score", f"{plagiarism_percent}%")
                    st.markdown('</div>', unsafe_allow_html=True)

                with p2:
                    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
                    st.subheader("Sentence Match Table")
                    if not sentence_df.empty:
                        st.dataframe(sentence_df, use_container_width=True, height=380)
                    else:
                        st.info("No sentence-level matches available.")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Add reference/original text to run plagiarism comparison.")

        with tab4:
            st.markdown('<div class="panel-card">', unsafe_allow_html=True)
            st.subheader("Highlighted Matched Sentences")
            if reference_text.strip() and not sentence_df.empty:
                st.markdown(highlighted_matches_html(sentence_df), unsafe_allow_html=True)
            else:
                st.info("Provide reference text to see highlighted matches.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.info("High similarity may indicate plagiarism or close paraphrasing. Manual review is still necessary.")