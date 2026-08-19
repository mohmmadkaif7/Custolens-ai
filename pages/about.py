import requests
import streamlit as st
from src.ui import inject_styles

inject_styles()
st.markdown('<div class="page-kicker">About the project</div>', unsafe_allow_html=True)
st.title("About CustoLens")
st.markdown('<div class="page-subtitle">An explainable customer intelligence platform built around segmentation, prediction and business strategy.</div>', unsafe_allow_html=True)

a,b = st.columns(2)
with a:
    st.markdown("""
    <div class="info-card">
    <h3>What it does</h3>
    <p>CustoLens identifies customer groups from age, income, annual spending and purchase behavior. A Random Forest classifier then predicts the segment of a new customer.</p>
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

st.info("CustoLens is designed as a decision-support system: The model provides evidence and the business strategy layer turns that evidence into action.")

# ============================================================
# CUSTOMER SUPPORT
# ============================================================

st.divider()

st.header("💬 Need Help?")

st.write(
    "Have a question or facing an issue with CustoLens AI? "
    "Our support team is here to help."
)

with st.form("support_form"):

    name = st.text_input(
        "Name",
        placeholder="Enter your name"
    )

    email = st.text_input(
        "Email",
        placeholder="Enter your email address"
    )

    category = st.selectbox(
        "Issue Category",
        [
            "General Question",
            "CSV Upload Problem",
            "Prediction Issue",
            "Recommendation Issue",
            "API / Technical Issue",
            "Other"
        ]
    )

    message = st.text_area(
        "Message",
        placeholder="Describe your question or issue...",
        height=150
    )

    submitted = st.form_submit_button(
        "📩 Submit Support Request",
        use_container_width=True
    )


# ============================================================
# SEND SUPPORT REQUEST
# ============================================================

if submitted:

    if not name.strip():

        st.error("Please enter your name.")

    elif not email.strip():

        st.error("Please enter your email address.")

    elif not message.strip():

        st.error("Please describe your issue.")

    else:

        payload = {
            "name": name.strip(),
            "email": email.strip(),
            "category": category,
            "message": message.strip()
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/support",
                json=payload,
                timeout=15
            )

            if response.status_code == 200:

                st.success(
                    "✅ Your support request has been "
                    "submitted successfully!"
                )

                st.info(
                    "Our support team will get back to you "
                    "as soon as possible."
                )

            else:

                try:
                    detail = response.json().get(
                        "detail",
                        "Unable to submit support request."
                    )

                except Exception:

                    detail = (
                        "Unable to submit support request."
                    )

                st.error(
                    f"❌ {detail}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Unable to connect to the CustoLens AI "
                "backend. Please make sure FastAPI is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "❌ The request timed out. Please try again."
            )

        except Exception:

            st.error(
                "❌ Something went wrong while submitting "
                "your support request."
            )