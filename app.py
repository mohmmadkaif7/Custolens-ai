import os
import streamlit as st

st.set_page_config(
    page_title="CustoLens",
    page_icon=":material/insights:",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.ui import inject_styles

# Load global UI styling
inject_styles()


# ============================================================
# LOGO
# ============================================================

LOGO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "custolens_logo.png",
)

# Single CustoLens logo at the top of the sidebar
st.logo(
    LOGO_PATH,
    size="large",
)


# ============================================================
# APPLICATION NAVIGATION
# ============================================================

pages = [
    st.Page(
        "pages/home.py",
        title="Home",
        icon=":material/home:",
        default=True,
    ),

    st.Page(
        "pages/customer_prediction.py",
        title="Customer Prediction",
        icon=":material/person_search:",
    ),

    st.Page(
        "pages/batch_analysis.py",
        title="Batch Analysis",
        icon=":material/upload_file:",
    ),

    st.Page(
        "pages/dashboard.py",
        title="Model Analytics",
        icon=":material/analytics:",
    ),

    st.Page(
        "pages/business_strategies.py",
        title="Business Strategies",
        icon=":material/strategy:",
    ),

    st.Page(
        "pages/about.py",
        title="About",
        icon=":material/info:",
    ),
]


# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation(
    pages,
    position="sidebar",
)

pg.run()