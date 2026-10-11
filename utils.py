import re
import string
from collections import Counter

import nltk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import torch
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModelForCausalLM, AutoTokenizer

for pkg in ["punkt", "stopwords"]:
    nltk.download(pkg, quiet=True)


def inject_global_css():
    import streamlit as st

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #f6f7fb 0%, #eef2ff 100%);
        color: #111827;
    }

    .block-container {
        max-width: 100% !important;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1220 0%, #111827 55%, #172554 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .auth-card {
        background: rgba(255,255,255,0.96);
        border: 1px solid #e5e7eb;
        border-radius: 28px;
        padding: 34px 34px 26px 34px;
        box-shadow: 0 18px 45px rgba(15,23,42,0.10);
    }

    .auth-icon {
        width: 78px;
        height: 78px;
        margin: 0 auto 18px auto;
        border-radius: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        font-size: 34px;
        font-weight: 800;
    }

    .auth-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 8px;
        letter-spacing: -0.8px;
    }

    .auth-subtitle {
        text-align: center;
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 28px;
    }

    .field-label {
        font-size: 14px;
        font-weight: 700;
        color: #111827;
        margin: 12px 0 8px 0;
    }

    .helper-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 14px;
        color: #374151;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .helper-link {
        color: #374151;
        text-decoration: none;
        font-weight: 500;
    }

    .divider-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 18px 0 18px 0;
        color: #6b7280;
        font-size: 14px;
        justify-content: center;
    }

    .divider-line {
        flex: 1;
        height: 1px;
        background: #e5e7eb;
    }

    .social-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-bottom: 18px;
    }

    .social-box {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 14px 16px;
        text-align: center;
        font-weight: 700;
        color: #111827;
        box-shadow: 0 4px 12px rgba(15,23,42,0.03);
    }

    .bottom-note {
        text-align: center;
        font-size: 15px;
        color: #6b7280;
        margin-top: 8px;
    }

    .bottom-note a {
        color: #111827;
        font-weight: 700;
        text-decoration: none;
    }

    .stTextInput input {
        height: 54px !important;
        border-radius: 16px !important;
        border: 1px solid #e5e7eb !important;
        background: #fbfbfd !important;
        color: #111827 !important;
        box-shadow: none !important;
        padding-left: 16px !important;
    }

    .stTextInput input:focus {
        border: 1px solid #a78bfa !important;
        box-shadow: 0 0 0 4px rgba(167,139,250,0.14) !important;
    }

    .stButton > button {
        width: 100%;
        height: 54px;
        border: none;
        border-radius: 16px;
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
        color: white;
        font-weight: 800;
        font-size: 17px;
        box-shadow: 0 12px 24px rgba(99,102,241,0.22);
    }

    .stButton > button:hover {
        filter: brightness(1.03);
    }

    .stCheckbox {
        margin-top: 4px;
    }

    .page-hero {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 55%, #ec4899 100%);
        color: white;
        padding: 26px 28px;
        border-radius: 24px;
        margin-bottom: 18px;
        box-shadow: 0 16px 36px rgba(37,99,235,0.18);
    }

    .page-hero-title {
        font-size: 34px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .page-hero-sub {
        font-size: 16px;
        opacity: 0.95;
    }

    .panel-card {
        background: rgba(255,255,255,0.92);
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 12px 24px rgba(15,23,42,0.06);
        margin-bottom: 18px;
    }

    .ui-stat {
        border-radius: 20px;
        padding: 18px;
        color: white;
        box-shadow: 0 14px 28px rgba(15,23,42,0.10);
    }

    .blue { background: linear-gradient(135deg, #2563eb, #06b6d4); }
    .purple { background: linear-gradient(135deg, #7c3aed, #ec4899); }
    .pink { background: linear-gradient(135deg, #f59e0b, #ef4444); }

    .ui-stat-label {
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 8px;
        opacity: 0.95;
    }

    .ui-stat-value {
        font-size: 18px;
        font-weight: 900;
    }

    .metric-shell {
        background: rgba(255,255,255,0.92);
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 16px;
        box-shadow: 0 10px 20px rgba(15,23,42,0.05);
        min-height: 120px;
    }

    .good-box, .warn-box, .bad-box {
        padding: 14px;
        border-radius: 16px;
        font-weight: 800;
        text-align: center;
    }

    .good-box {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        color: #166534;
        border: 1px solid #86efac;
    }

    .warn-box {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: #92400e;
        border: 1px solid #fbbf24;
    }

    .bad-box {
        background: linear-gradient(135deg, #fecaca, #fda4af);
        color: #881337;
        border: 1px solid #fb7185;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 14px;
        font-weight: 700;
    }

    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_resource
def load_gpt_model():
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    return tokenizer, model


@st.cache_resource
def load_sentence_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def clean_tokens(text):
    stop_words = set(stopwords.words("english"))
    tokens = nltk.word_tokenize(text.lower())
    return [
        token for token in tokens
        if token not in stop_words
        and token not in string.punctuation
        and token.strip() != ""
    ]


def split_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return [s.strip() for s in sentences if s.strip()]


def calculate_perplexity(text):
    tokenizer, gpt_model = load_gpt_model()

    text = clean_text(text)
    encodings = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    input_ids = encodings["input_ids"]
    attention_mask = encodings["attention_mask"]

    with torch.no_grad():
        outputs = gpt_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=input_ids
        )
        loss = outputs.loss

    return float(torch.exp(loss).item())


def calculate_burstiness(text):
    tokens = clean_tokens(text)
    if not tokens:
        return 0.0
    freq = FreqDist(tokens)
    repeated_words = sum(1 for count in freq.values() if count > 1)
    return repeated_words / len(freq)


def lexical_diversity(text):
    tokens = clean_tokens(text)
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def repetition_ratio(text):
    tokens = clean_tokens(text)
    if not tokens:
        return 0.0
    freq = Counter(tokens)
    repeated_total = sum(count for _, count in freq.items() if count > 1)
    return repeated_total / len(tokens)


def average_sentence_length(text):
    sentences = split_sentences(text)
    if not sentences:
        return 0.0
    lengths = [len(nltk.word_tokenize(s)) for s in sentences]
    return sum(lengths) / len(lengths)


def sentence_length_variation(text):
    sentences = split_sentences(text)
    if len(sentences) < 2:
        return 0.0
    lengths = [len(nltk.word_tokenize(s)) for s in sentences]
    mean_len = sum(lengths) / len(lengths)
    if mean_len == 0:
        return 0.0
    variance = sum((x - mean_len) ** 2 for x in lengths) / len(lengths)
    return variance / mean_len


def normalize_perplexity(pp):
    if pp < 20:
        return 1.0
    if pp < 40:
        return 0.85
    if pp < 60:
        return 0.70
    if pp < 100:
        return 0.50
    if pp < 200:
        return 0.30
    return 0.10


def detect_ai(text):
    pp = calculate_perplexity(text)
    burst = calculate_burstiness(text)
    lex_div = lexical_diversity(text)
    rep_ratio = repetition_ratio(text)
    avg_sent_len = average_sentence_length(text)
    sent_var = sentence_length_variation(text)

    ai_score = (
        0.35 * normalize_perplexity(pp) +
        0.15 * (1 - min(burst, 1.0)) +
        0.15 * (1 - min(lex_div, 1.0)) +
        0.15 * min(rep_ratio, 1.0) +
        0.10 * (1 - min(sent_var, 1.0)) +
        0.10 * (1 if avg_sent_len < 18 else 0.4)
    ) * 100

    if ai_score >= 70:
        label = "Likely AI-generated"
    elif ai_score >= 45:
        label = "Possibly AI-generated"
    else:
        label = "Likely human-written"

    return {
        "Perplexity": round(pp, 2),
        "Burstiness": round(burst, 4),
        "Lexical Diversity": round(lex_div, 4),
        "Repetition Ratio": round(rep_ratio, 4),
        "Average Sentence Length": round(avg_sent_len, 2),
        "Sentence Variation": round(sent_var, 4),
        "AI Score": round(ai_score, 2),
        "Result": label
    }


def semantic_similarity_score(text1, text2):
    sentence_model = load_sentence_model()
    text1 = clean_text(text1)
    text2 = clean_text(text2)
    embeddings = sentence_model.encode([text1, text2])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(score)


def plagiarism_result(score):
    percent = score * 100
    if percent >= 85:
        label = "High similarity - possible plagiarism"
    elif percent >= 60:
        label = "Moderate similarity"
    elif percent >= 35:
        label = "Low similarity"
    else:
        label = "Very low similarity"
    return round(percent, 2), label


def sentence_level_matches(input_text, reference_text):
    sentence_model = load_sentence_model()

    input_sentences = split_sentences(input_text)
    ref_sentences = split_sentences(reference_text)

    if not input_sentences or not ref_sentences:
        return pd.DataFrame(columns=[
            "Input Sentence",
            "Best Matching Reference Sentence",
            "Similarity %",
            "Flag"
        ])

    input_embeddings = sentence_model.encode(input_sentences)
    ref_embeddings = sentence_model.encode(ref_sentences)

    rows = []
    for i, inp_emb in enumerate(input_embeddings):
        sims = cosine_similarity([inp_emb], ref_embeddings)[0]
        best_idx = sims.argmax()
        best_score = float(sims[best_idx] * 100)

        if best_score >= 85:
            flag = "🔴 High"
        elif best_score >= 60:
            flag = "🟡 Medium"
        else:
            flag = "🟢 Low"

        rows.append({
            "Input Sentence": input_sentences[i],
            "Best Matching Reference Sentence": ref_sentences[best_idx],
            "Similarity %": round(best_score, 2),
            "Flag": flag
        })

    df = pd.DataFrame(rows)
    df = df.sort_values(by="Similarity %", ascending=False).reset_index(drop=True)
    return df


def highlighted_matches_html(sentence_df):
    if sentence_df.empty:
        return "<p>No sentence-level matches available.</p>"

    blocks = []
    for _, row in sentence_df.iterrows():
        score = row["Similarity %"]
        if score >= 85:
            bg = "#fee2e2"
            border = "#ef4444"
        elif score >= 60:
            bg = "#fef3c7"
            border = "#f59e0b"
        else:
            bg = "#dcfce7"
            border = "#22c55e"

        blocks.append(f"""
        <div style="
            background:{bg};
            border-left:6px solid {border};
            padding:14px;
            border-radius:12px;
            margin-bottom:12px;">
            <div style="font-weight:700; margin-bottom:6px;">Input Sentence</div>
            <div style="margin-bottom:10px;">{row["Input Sentence"]}</div>
            <div style="font-weight:700; margin-bottom:6px;">Best Matching Reference Sentence</div>
            <div style="margin-bottom:10px;">{row["Best Matching Reference Sentence"]}</div>
            <div style="font-weight:700;">Similarity: {row["Similarity %"]}% &nbsp; {row["Flag"]}</div>
        </div>
        """)
    return "".join(blocks)


def plot_top_words(text):
    tokens = clean_tokens(text)
    if not tokens:
        st.warning("No meaningful words found to plot.")
        return

    counts = Counter(tokens).most_common(10)
    words = [w for w, _ in counts]
    values = [c for _, c in counts]

    fig = px.bar(
        x=words,
        y=values,
        labels={"x": "Words", "y": "Count"},
        title="Top 10 Repeated Words"
    )
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#111827"
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_metrics(ai_result, plagiarism_percent):
    df = pd.DataFrame({
        "Metric": [
            "Perplexity",
            "Burstiness",
            "Lexical Diversity",
            "Repetition Ratio",
            "Sentence Variation",
            "AI Score",
            "Similarity %"
        ],
        "Value": [
            ai_result["Perplexity"],
            ai_result["Burstiness"],
            ai_result["Lexical Diversity"],
            ai_result["Repetition Ratio"],
            ai_result["Sentence Variation"],
            ai_result["AI Score"],
            plagiarism_percent
        ]
    })

    fig = px.bar(df, x="Metric", y="Value", title="Analysis Overview")
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#111827"
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_ai_pie_chart(ai_score):
    human_score = max(0, 100 - ai_score)

    df = pd.DataFrame({
        "Label": ["AI Probability", "Human Probability"],
        "Value": [ai_score, human_score]
    })

    fig = px.pie(
        df,
        names="Label",
        values="Value",
        title="AI vs Human Probability",
        hole=0.45
    )
    fig.update_layout(
        paper_bgcolor="white",
        font_color="#111827"
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_sentence_similarity_distribution(sentence_df):
    if sentence_df.empty:
        st.info("No sentence similarity data available.")
        return

    chart_df = sentence_df.copy()
    chart_df["Sentence No"] = range(1, len(chart_df) + 1)

    fig = px.line(
        chart_df,
        x="Sentence No",
        y="Similarity %",
        markers=True,
        title="Sentence Similarity Distribution"
    )
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#111827",
        xaxis_title="Sentence Number",
        yaxis_title="Similarity %"
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_plagiarism_gauge(plagiarism_percent):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=plagiarism_percent,
        title={"text": "Plagiarism %"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 35], "color": "#dcfce7"},
                {"range": [35, 60], "color": "#fef3c7"},
                {"range": [60, 100], "color": "#fee2e2"}
            ]
        }
    ))

    fig.update_layout(
        paper_bgcolor="white",
        font_color="#111827",
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)