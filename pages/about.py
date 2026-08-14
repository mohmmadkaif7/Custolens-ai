
import streamlit as st
from src.ui import inject_styles

inject_styles()
st.markdown('<div class="page-kicker">About the project</div>', unsafe_allow_html=True)
st.title("About CustoLens AI")
st.markdown('<div class="page-subtitle">An explainable customer intelligence platform built around segmentation, prediction and business strategy.</div>', unsafe_allow_html=True)

a,b = st.columns(2)
with a:
    st.markdown("""
    <div class="info-card">
    <h3>What it does</h3>
    <p>CustoLens AI identifies customer groups from age, income, annual spending and purchase behavior. A Random Forest classifier then predicts the segment of a new customer.</p>
    <p>The platform goes one step further by explaining the result and connecting each segment to business actions.</p>
    </div>
    """, unsafe_allow_html=True)
with b:
    st.markdown("""
    <div class="info-card">
    <h3>Technology</h3>
    <p><b>Python</b> · Streamlit · Pandas · Scikit-learn · Plotly · FastAPI · Joblib</p>
    <p><b>ML:</b> K-Means customer segmentation + Random Forest classification.</p>
    <p><b>UX:</b> Interactive dashboard, filtering, batch analysis and explainable predictions.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### End-to-end flow")
st.markdown("""
1. **Prepare** customer data and normalize common column formats.
2. **Segment** customers into Premium, Regular and Budget groups.
3. **Train / predict** using the Random Forest classifier.
4. **Explain** the prediction using local feature sensitivity and segment benchmarks.
5. **Act** using segment-specific business strategies.
""")

st.info("CustoLens AI is designed as a decision-support system: the model provides evidence and the business strategy layer turns that evidence into action.")
