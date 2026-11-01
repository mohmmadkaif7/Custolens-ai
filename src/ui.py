import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

SEGMENTS = ["Premium", "Regular", "Budget"]
SEGMENT_COLORS = {
    "Premium": "#7C3AED",
    "Regular": "#2563EB",
    "Budget": "#14B8A6",
}

def data_path(filename):
    return os.path.join(DATA_DIR, filename)

@st.cache_data
def load_customer_data():
    return pd.read_csv(data_path("customer_segmented.csv"))

@st.cache_data
def load_recommendation_data():
    return pd.read_csv(data_path("customer_recommendations.csv"))

@st.cache_data
def load_test_data():
    return pd.read_csv(data_path("test_customers.csv"))

def money(value):
    try:
        return f"₹{float(value):,.0f}"
    except Exception:
        return "—"

def segment_counts(df, column="segment"):
    if column not in df.columns:
        return pd.Series(dtype="int64")
    return df[column].value_counts().reindex(SEGMENTS).fillna(0)

def inject_styles():
    st.markdown("""
    <style>
    /* ==================== APP ==================== */
    .stApp, [data-testid="stAppViewContainer"] {
        background: #f8fafc;
        color: #172033;
    }
    [data-testid="stHeader"] {
        background: rgba(248,250,252,.92);
    }
    .block-container {
        max-width: 1440px;
        padding-top: 1.65rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3, h4 {
        color: #14213d !important;
        letter-spacing: -0.025em;
    }
    p, label, .stMarkdown {
        color: #526174;
    }

    /* ==================== SIDEBAR ==================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #071A3A 0%, #0A2348 55%, #071A3A 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }
    section[data-testid="stSidebar"] > div {
        padding: .75rem .9rem 1rem .9rem;
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p {
        color: #dbe7ff !important;
    }


    /* Streamlit's native navigation */
    [data-testid="stSidebarNav"] {
        padding: 0 2px !important;
    }
    [data-testid="stSidebarNav"] ul {
        gap: 5px !important;
    }
    [data-testid="stSidebarNav"] li {
        margin: 0 !important;
    }
    [data-testid="stSidebarNav"] a {
        border-radius: 11px !important;
        color: #D8E3F8 !important;
        font-weight: 650 !important;
        padding: .62rem .72rem !important;
        transition: all .18s ease;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(139,92,246,.14) !important;
        color: #fff !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(90deg,#7C3AED 0%,#8B5CF6 100%) !important;
        color: #fff !important;
        box-shadow: 0 7px 18px rgba(124,58,237,.28);
    }
    [data-testid="stSidebarNav"] a svg {
        color: currentColor !important;
    }

    /* ==================== PAGE ==================== */
    .page-kicker {
        color: #7C3AED;
        font-size: .74rem;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: .13em;
        margin-bottom: .25rem;
    }
    .page-subtitle {
        color: #667085;
        font-size: .96rem;
        margin-bottom: 1.35rem;
    }
    .hero {
        background: linear-gradient(135deg,#ffffff 0%,#f5f1ff 100%);
        border: 1px solid #e9ddff;
        border-radius: 24px;
        padding: 42px 44px;
        margin: 7px 0 25px;
        box-shadow: 0 14px 38px rgba(31,41,55,.06);
    }
    .hero-title {
        font-size: 2.75rem;
        line-height: 1.04;
        font-weight: 880;
        color: #14213d;
        max-width: 820px;
        margin-bottom: 14px;
    }
    .hero-copy {
        font-size: 1.02rem;
        line-height: 1.65;
        color: #667085;
        max-width: 800px;
    }
    .feature-card, .metric-card, .info-card, .result-card, .strategy-card, .reason-card {
        background: #fff;
        border: 1px solid #e7eaf0;
        border-radius: 17px;
        box-shadow: 0 8px 25px rgba(30,41,59,.045);
    }
    .feature-card {
        padding: 20px;
        min-height: 145px;
        margin-bottom: 14px;
    }
    .feature-icon { font-size: 1.4rem; margin-bottom: 9px; }
    .feature-title { font-weight: 780; color: #172033; font-size: 1rem; margin-bottom: 5px; }
    .feature-copy { color: #718096; font-size: .86rem; line-height: 1.5; }

    .metric-card {
        padding: 17px 18px;
        min-height: 104px;
    }
    .metric-label {
        font-size: .72rem; color: #718096; font-weight: 750;
        text-transform: uppercase; letter-spacing: .05em;
    }
    .metric-value { font-size: 1.75rem; color: #172033; font-weight: 850; margin-top: 3px; }
    .metric-note { font-size: .75rem; color: #98A2B3; margin-top: 2px; }

    .section-label {
        color: #14213d;
        font-size: 1.05rem;
        font-weight: 800;
        margin: 1.2rem 0 .65rem;
    }
    .info-card { padding: 18px 20px; }
    .result-card { padding: 24px; min-height: 260px; }
    .result-segment { font-size: 2.15rem; font-weight: 900; color: #7C3AED; margin: 7px 0 9px; }
    .confidence {
        display:inline-block; padding:5px 10px; border-radius:999px;
        background:#F1EAFE; color:#6D28D9; font-size:.76rem; font-weight:800;
    }
    .reason-card {
        padding: 15px 17px;
        margin: 8px 0;
        border-left: 4px solid #8B5CF6;
    }
    .reason-title { color:#172033; font-weight:800; font-size:.9rem; }
    .reason-copy { color:#667085; font-size:.82rem; line-height:1.45; margin-top:3px; }

    .strategy-card {
    padding: 24px;
    min-height: 320px;
    box-sizing: border-box;
}

.strategy-badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: .73rem;
    font-weight: 850;
    background: #F1EAFE;
    color: #6D28D9;
}

.strategy-title {
    font-size: 1.45rem;
    font-weight: 850;
    color: #172033;
    margin: 10px 0 5px;
    line-height: 1.35;
    min-height: 78px;
}

.strategy-goal {
    color: #667085;
    font-size: .86rem;
    line-height: 1.5;
    min-height: 78px;
}

.strategy-list {
    color: #526174;
    font-size: .86rem;
    line-height: 1.8;
    padding-left: 18px;
    margin-top: 18px;
}

/* Equal-height strategy columns */
div[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    display: flex !important;
    align-items: stretch !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div {
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
}

.strategy-card-equal {
    width: 100% !important;
    height: 700px !important;
    min-height: 700px !important;
}

    .upload-zone {
        border: 1.5px dashed #C4B5FD;
        background: #FFFFFF;
        border-radius: 17px;
        padding: 28px 24px;
        text-align: center;
        color: #526174;
        box-shadow: 0 8px 25px rgba(30,41,59,.045);
    }
    .upload-title {
        color: #172033;
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .upload-copy {
        color: #526174;
        font-size: .92rem;
    }
    .upload-hint {
        color: #98A2B3;
        font-size: .78rem;
        margin-top: 6px;
    }
    .analysis-info {
        background: #FFFFFF;
        border: 1px solid #E7EAF0;
        border-radius: 12px;
        padding: 12px 15px;
        color: #667085;
        font-size: .86rem;
        margin-bottom: 12px;
    }
    .table-card {
        background: #FFFFFF;
        border: 1px solid #E7EAF0;
        border-radius: 14px;
        padding: 8px;
        overflow: hidden;
    }

    .prediction-action-card {
        min-height: 430px;
    }
    .prediction-divider {
        height: 1px;
        background: #E9EDF3;
        margin: 20px 0 16px;
    }
    .recommendation-heading {
        color: #172033;
        font-size: .78rem;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: .05em;
        margin-bottom: 5px;
    }
    .action-heading { margin-top: 16px; }
    .prediction-action-card .recommendation-strategy {
        color: #6D28D9;
        font-size: 1rem;
        font-weight: 850;
        line-height: 1.35;
    }
    .prediction-action-card .recommendation-list {
        margin: 6px 0 0;
        padding-left: 19px;
        color: #526174;
        font-size: .86rem;
        line-height: 1.65;
    }
    .recommendation-box {
        background: #FFFFFF;
        border: 1px solid #DDD6FE;
        border-left: 5px solid #8B5CF6;
        border-radius: 17px;
        padding: 20px 22px;
        box-shadow: 0 8px 25px rgba(30,41,59,.045);
        margin-bottom: 1rem;
    }
    .recommendation-strategy {
        color: #6D28D9;
        font-size: 1.05rem;
        font-weight: 850;
        margin-bottom: 8px;
    }
    .recommendation-list {
        color: #526174;
        font-size: .9rem;
        line-height: 1.7;
    }
   .strategy-card-equal {
    height: 700px;
    min-height: 700px;
    box-sizing: border-box;
}

    .combined-tab-note {
        color: #667085;
        font-size: .88rem;
        margin: .1rem 0 1rem;
    }

    .model-panel {
        background: #FFFFFF;
        border: 1px solid #E7EAF0;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 7px 20px rgba(30,41,59,.04);
    }
    .metric-strip {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }
    .mini-metric {
        flex: 1 1 150px;
        background: #FFFFFF;
        border: 1px solid #E7EAF0;
        border-radius: 14px;
        padding: 14px 16px;
    }
    .mini-metric .label {
        color: #667085;
        font-size: .72rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: .04em;
    }
    .mini-metric .value {
        color: #172033;
        font-size: 1.45rem;
        font-weight: 850;
        margin-top: 4px;
    }
    .white-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: #FFFFFF;
        border: 1px solid #E7EAF0;
        border-radius: 12px;
        overflow: hidden;
        color: #334155;
        font-size: .84rem;
    }
    .white-table th {
        background: #F8FAFC;
        color: #475569;
        font-weight: 800;
        text-align: left;
        padding: 11px 12px;
        border-bottom: 1px solid #E7EAF0;
    }
    .white-table td {
        background: #FFFFFF;
        color: #334155;
        padding: 10px 12px;
        border-bottom: 1px solid #EEF2F6;
    }
    .white-table tr:last-child td { border-bottom: 0; }
    .white-table .segment-name { font-weight: 800; color: #172033; }

    /* Light number-input steppers */
    button[aria-label="Increment"],
    button[aria-label="Decrement"],
    button[data-testid="stNumberInputStepUp"],
    button[data-testid="stNumberInputStepDown"] {
        background: #F1ECFF !important;
        color: #6D28D9 !important;
        border-color: #E5DDFB !important;
    }
    button[aria-label="Increment"]:hover,
    button[aria-label="Decrement"]:hover,
    button[data-testid="stNumberInputStepUp"]:hover,
    button[data-testid="stNumberInputStepDown"]:hover {
        background: #E7DEFF !important;
        color: #5B21B6 !important;
    }

    /* Light purple purchase-frequency slider */
    div[data-baseweb="slider"] [role="slider"] {
        background: #C4B5FD !important;
        border: 2px solid #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,.12) !important;
    }
    div[data-baseweb="slider"] [role="progressbar"],
    div[data-baseweb="slider"] [data-testid="stSliderTrack"] {
        background: #C4B5FD !important;
    }
    div[data-baseweb="slider"] > div > div > div {
        background: #C4B5FD !important;
    }

    /* ==================== CONTROLS ==================== */
    .stButton > button {
        width: 100%;
        border-radius: 10px !important;
        border: 1px solid #7C3AED !important;
        background: linear-gradient(90deg,#7C3AED,#8B5CF6) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 760 !important;
        padding: .55rem 1rem !important;
    }
    .stButton > button *,
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    .stButton > button:hover {
        border-color:#6D28D9;
        background:#8B5CF6;
        color:#000000 !important;
    }
    .stDownloadButton > button {
        width: 100%;
        border-radius: 10px !important;
        font-weight: 760 !important;
        border: 1px solid #7C3AED !important;
        background: linear-gradient(90deg,#7C3AED,#8B5CF6) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    .stDownloadButton > button *,
    .stDownloadButton > button p,
    .stDownloadButton > button span,
    .stDownloadButton > button div {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    .stDownloadButton > button:hover {
        background: #8B5CF6 !important;
        color: #000000 !important;
    }
    /* Keep form controls bright and readable even when the user's Streamlit theme is dark. */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] {
        background: #FFFFFF !important;
        border-color: #D9DDE7 !important;
        color: #172033 !important;
    }
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background: #FFFFFF !important;
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
    }
    div[data-baseweb="select"] input {
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
    }
    div[data-baseweb="slider"] [role="slider"] {
        background: #C4B5FD !important;
        border: 2px solid #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,.12) !important;
    }
    div[data-baseweb="slider"] [data-testid="stTickBarMin"],
    div[data-baseweb="slider"] [data-testid="stTickBarMax"] {
        color: #667085 !important;
    }
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"],
    [data-testid="stSidebarCollapseButton"] button {
        color: #FFFFFF !important;
        background: #17345F !important;
        border: 1px solid rgba(255,255,255,.22) !important;
        border-radius: 8px !important;
        opacity: 1 !important;
        box-shadow: 0 2px 8px rgba(7,26,58,.18) !important;
    }
    button[aria-label="Close sidebar"] svg,
    button[aria-label="Open sidebar"] svg,
    [data-testid="stSidebarCollapseButton"] button svg {
        color: #FFFFFF !important;
        stroke: #FFFFFF !important;
        opacity: 1 !important;
    }
    button[aria-label="Open sidebar"] {
        position: fixed !important;
        top: .7rem !important;
        left: .7rem !important;
        z-index: 999999 !important;
    }

    /* File uploader: white, clean and readable. */
    section[data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF !important;
        border: 1.5px dashed #C4B5FD !important;
        border-radius: 14px !important;
    }
    section[data-testid="stFileUploaderDropzone"] button {
        background: #F1ECFF !important;
        border: 1px solid #DDD6FE !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    section[data-testid="stFileUploaderDropzone"] button *,
    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone small"] {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* Streamlit dataframe container stays white. */
    [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border: 1px solid #E7EAF0 !important;
        border-radius: 10px !important;
    }
    [data-testid="stDataFrame"] iframe {
        background: #FFFFFF !important;
    }

    [data-testid="stMetric"] {
        background:#fff; border:1px solid #E7EAF0; border-radius:14px;
        padding:14px 16px;
    }
    hr { border-color:#E9EDF3; }
    </style>
    """, unsafe_allow_html=True)

def show_plotly(fig, **kwargs):
    """Render Plotly charts with a light professional theme and no modebar."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#334155", family="Arial, sans-serif", size=13),
        title_font=dict(color="#172033", size=17),
        xaxis=dict(
            title_font=dict(color="#334155", size=13),
            tickfont=dict(color="#475569", size=12),
            linecolor="#CBD5E1",
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
        ),
        yaxis=dict(
            title_font=dict(color="#334155", size=13),
            tickfont=dict(color="#475569", size=12),
            linecolor="#CBD5E1",
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
        ),
        legend=dict(font=dict(color="#334155", size=12)),
    )
    config = {"displayModeBar": False, "displaylogo": False}
    config.update(kwargs.pop("config", {}))
    return st.plotly_chart(fig, config=config, **kwargs)

def page_header(kicker, title, subtitle):
    st.markdown(f'<div class="page-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def card_metric(label, value, note=""):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True
    )

def segment_badge(segment):
    return f'<span class="strategy-badge">{segment}</span>'