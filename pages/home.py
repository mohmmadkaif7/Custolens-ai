import streamlit as st
from src.ui import inject_styles, load_customer_data

inject_styles()
df = load_customer_data()

st.markdown("""
<div class="hero">
  <div class="hero-title">Turn customer behavior into actionable business strategies.</div>
  <div class="hero-copy">
    CustoLens AI uses customer data, machine learning and explainable insights
    to identify meaningful segments, predict customer value and turn those
    insights into practical business actions.
  </div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
for col, label, value, note in [
    (c1, "Customers", f"{len(df):,}", "Training records"),
    (c2, "Segments", "3", "Premium · Regular · Budget"),
]:
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
            unsafe_allow_html=True
        )

st.markdown("### Explore CustoLens AI")
features = [
    ("📊", "Dashboard", "Get the complete customer picture at a glance."),
    ("🎯", "Customer Prediction", "Predict a customer's segment and understand the result."),
    ("📤", "Batch Analysis", "Upload a CSV, filter it, analyze it and download predictions."),
    ("📈", "Analytics", "Explore interactive behavior, value and model-quality charts."),
    ("💡", "Business Strategies", "Turn every segment into clear business actions."),
]
cols = st.columns(3)
for i, (icon, title, copy) in enumerate(features):
    with cols[i % 3]:
        st.markdown(
            f'<div class="feature-card"><div class="feature-icon">{icon}</div>'
            f'<div class="feature-title">{title}</div><div class="feature-copy">{copy}</div></div>',
            unsafe_allow_html=True
        )

st.info("Start with Dashboard for the overall picture, or use Customer Prediction for a live AI demonstration.")
