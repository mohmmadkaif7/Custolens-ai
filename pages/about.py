import streamlit as st
from urllib.parse import quote

from src.ui import inject_styles


inject_styles()

st.markdown(
    '<div class="page-kicker">About the project</div>',
    unsafe_allow_html=True
)

st.title("About CustoLens")

st.markdown(
    '<div class="page-subtitle">'
    'An explainable customer intelligence platform built around '
    'segmentation, prediction and business strategy.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# ABOUT CONTENT
# =========================================================

a, b = st.columns(2)

with a:

    st.markdown("""
    <div class="info-card">

    <h3>What it does</h3>

    <p>
    CustoLens identifies customer groups from age, income,
    annual spending and purchase behavior. A Random Forest
    classifier then predicts the segment of a new customer.
    </p>

    <p>
    The platform goes one step further by explaining the
    result and connecting each segment to business actions.
    </p>

    </div>
    """, unsafe_allow_html=True)


with b:

    st.markdown("""
    <div class="info-card">

    <h3>Technology</h3>

    <p>
    <b>Python</b> · Streamlit · Pandas · Scikit-learn ·
    Plotly · FastAPI · Joblib
    </p>

    <p>
    <b>ML:</b> K-Means customer segmentation +
    Random Forest classification.
    </p>

    <p>
    <b>UX:</b> Interactive dashboard, filtering,
    batch analysis and explainable predictions.
    </p>

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


st.info(
    "CustoLens is designed as a decision-support system: "
    "The model provides evidence and the business strategy "
    "layer turns that evidence into action."
)


# =========================================================
# CUSTOMER SUPPORT
# =========================================================

st.markdown("---")

st.markdown("## 💬 Need Help?")

st.write(
    "Have a question or facing an issue with CustoLens ? "
    "Our support team is here to help."
)


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
        "Technical Issue",
        "Prediction Issue",
        "CSV Upload Issue",
        "Recommendation Issue",
        "Other"
    ]
)

message = st.text_area(
    "Message",
    placeholder="Describe your question or issue...",
    height=150
)


if st.button(
    "📩 Submit Support Request",
    use_container_width=True
):

    if not name.strip():

        st.warning("Please enter your name.")

    elif not email.strip():

        st.warning("Please enter your email.")

    elif not message.strip():

        st.warning("Please describe your issue.")

    else:

        subject = (
            f"CustoLens Support - {category}"
        )

        body = f"""Hello CustoLens Support Team,

Name: {name}
Email: {email}
Issue Category: {category}

Message:
{message}

Thank you.
"""

        mailto_link = (
            "mailto:custolens@gmail.com"
            f"?subject={quote(subject)}"
            f"&body={quote(body)}"
        )

        st.markdown(
            f"""
            <meta http-equiv="refresh"
                  content="0; url={mailto_link}">
            """,
            unsafe_allow_html=True
        )

        st.success(
            "Opening your email application..."
        )