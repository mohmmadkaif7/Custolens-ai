import streamlit as st
from src.ui import inject_styles, page_header, load_customer_data
from src.prediction_pipeline import predict_customer_details

inject_styles()
df = load_customer_data()

page_header(
    "AI Prediction",
    "Customer Prediction",
    "Predict a customer segment and immediately see the recommended business action."
)

left, right = st.columns([0.95, 1.05], gap="large")

with left:
    st.markdown("### Customer profile")

    age = st.number_input(
        "Age", min_value=18, max_value=100, value=32, step=1
    )
    income = st.number_input(
        "Annual Income (₹)", min_value=0.0, value=1200000.0, step=50000.0
    )
    spending = st.number_input(
        "Annual Spending (₹)", min_value=0.0, value=150000.0, step=5000.0
    )
    frequency = st.slider(
        "Purchase Frequency",
        0.0,
        1.0,
        float(df["purchase_frequency"].median()),
        0.05,
    )

    st.caption("The model uses the same 0–1 purchase-frequency scale as the trained data.")
    predict_clicked = st.button("Analyze Customer", use_container_width=True)

with right:
    st.markdown("### Prediction & recommended action")

    if predict_clicked:
        result = predict_customer_details(
            age, income, frequency, spending, df
        )
        actions = result.get("recommendations", [])

        action_html = "".join(f"<li>{item}</li>" for item in actions)

        st.markdown(
            f"""
            <div class="result-card prediction-action-card">
              <div class="strategy-badge">PREDICTED SEGMENT</div>
              <div class="result-segment">{result["segment"]}</div>
              <span class="confidence">Model confidence · {result["confidence"]*100:.1f}%</span>

              <div class="prediction-divider"></div>

              <div class="recommendation-heading">Recommended Strategy</div>
              <div class="recommendation-strategy">{result["strategy"]}</div>

              <div class="recommendation-heading action-heading">Recommended Actions</div>
              <ul class="recommendation-list">
                {action_html}
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="result-card prediction-action-card">
              <div class="strategy-badge">READY</div>
              <div class="result-segment">—</div>
              <p>Enter the customer profile and select <b>Analyze Customer</b> to generate the segment and recommended strategy.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
