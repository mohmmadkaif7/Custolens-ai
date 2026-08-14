import streamlit as st
import pandas as pd
import plotly.express as px

from src.ui import inject_styles, page_header, show_plotly
from src.data_adapter import prepare_customer_data
from src.prediction_pipeline import predict_customer_segment


# ============================================================
# BATCH ANALYSIS
# ============================================================

inject_styles()

page_header(
    "Batch Intelligence",
    "Batch Analysis",
    "Upload customer data, analyze the complete dataset and generate segment predictions."
)


# ============================================================
# UPLOAD
# ============================================================

st.markdown(
    """
    <div class="upload-zone">
        <div class="upload-title">Upload customer data</div>
        <div class="upload-copy">
            Drag and drop a CSV file below, or browse your files.
        </div>
        <div class="upload-hint">
            The uploaded dataset will be analyzed using the trained customer segmentation model.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    label_visibility="collapsed",
)


if not uploaded:
    st.markdown("### Ready to analyze your customer data")

    a, b, c, d = st.columns(4)

    for col, icon, title, copy in [
        (
            a,
            "✓",
            "Upload CSV",
            "Upload the customer dataset you want to analyze.",
        ),
        (
            b,
            "✓",
            "Analyze",
            "Run the trained segmentation model on every valid customer.",
        ),
        (
            c,
            "✓",
            "View results",
            "See segment counts, distribution and the analyzed customer table.",
        ),
        (
            d,
            "✓",
            "Download",
            "Download the complete prediction results as a CSV file.",
        ),
    ]:
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-copy">{copy}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.stop()


# ============================================================
# READ UPLOADED CSV
# ============================================================

try:
    raw = pd.read_csv(uploaded)
except Exception as exc:
    st.error(f"Could not read this CSV: {exc}")
    st.stop()


st.success(
    f"Loaded {len(raw):,} rows and {len(raw.columns):,} columns."
)


# ============================================================
# ANALYZE CUSTOMER DATA
# ============================================================

st.markdown("### Analyze customer data")

st.markdown(
    """
    <div class="analysis-info">
        The complete uploaded dataset will be processed. No manual filters are applied.
    </div>
    """,
    unsafe_allow_html=True,
)

analyze_clicked = st.button(
    "Analyze Customer Data",
    use_container_width=True,
    key="analyze_customer_data",
)


if analyze_clicked:

    prepared, mapping, missing = prepare_customer_data(raw)

    if missing:
        st.error(
            "The uploaded file is missing model-ready information."
        )
        st.caption(
            "Required fields: age, income, purchase frequency and annual spending, "
            "or supported equivalents."
        )
        st.stop()

    progress = st.progress(0)
    predictions = []

    total_rows = len(prepared)

    for i, (_, row) in enumerate(prepared.iterrows(), start=1):
        predictions.append(
            predict_customer_segment(
                row["age"],
                row["income"],
                row["purchase_frequency"],
                row["annual_spending"],
            )
        )
        progress.progress(i / max(total_rows, 1))

    progress.empty()

    result = raw.loc[prepared.index].copy()
    result["predicted_segment"] = predictions

    st.session_state["batch_result"] = result


# ============================================================
# RESULTS
# ============================================================

if "batch_result" in st.session_state:

    result = st.session_state["batch_result"]

    st.markdown("---")
    st.markdown("## Batch analysis results")

    counts = (
        result["predicted_segment"]
        .value_counts()
        .reindex(["Premium", "Regular", "Budget"])
        .fillna(0)
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Customers Analyzed",
        f"{len(result):,}",
    )

    c2.metric(
        "Premium",
        f"{int(counts.get('Premium', 0)):,}",
    )

    c3.metric(
        "Regular",
        f"{int(counts.get('Regular', 0)):,}",
    )

    c4.metric(
        "Budget",
        f"{int(counts.get('Budget', 0)):,}",
    )

    # --------------------------------------------------------
    # Segment distribution
    # --------------------------------------------------------

    st.markdown("### Segment distribution")

    seg_counts = (
        counts
        .reset_index()
    )

    seg_counts.columns = [
        "Segment",
        "Customers",
    ]

    fig = px.pie(
        seg_counts,
        names="Segment",
        values="Customers",
        hole=0.58,
        color="Segment",
        color_discrete_map={
            "Premium": "#7C3AED",
            "Regular": "#2563EB",
            "Budget": "#14B8A6",
        },
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    fig.update_layout(
        title="Customer Segment Distribution",
        title_font=dict(
            color="#172033",
            size=18,
        ),
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10,
        ),
        legend_title="",
    )

    show_plotly(
        fig,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # Uploaded-data graphs
    # --------------------------------------------------------

    st.markdown("### Uploaded data insights")

    numeric_cols = raw.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_cols = [
        c
        for c in raw.columns
        if c not in numeric_cols
        and raw[c].nunique(dropna=True) <= 30
    ]

    graph_tabs = st.tabs(
        [
            "Distribution",
            "Numeric Relationships",
            "Category Breakdown",
        ]
    )

    with graph_tabs[0]:

        if numeric_cols:

            chosen = st.selectbox(
                "Numeric field",
                numeric_cols,
                key="batch_histogram_field",
            )

            fig = px.histogram(
                raw,
                x=chosen,
                nbins=25,
                title=f"{chosen.replace('_', ' ').title()} Distribution",
            )

            fig.update_layout(
                margin=dict(
                    l=10,
                    r=10,
                    t=55,
                    b=10,
                )
            )

            show_plotly(
                fig,
                use_container_width=True,
            )

        else:
            st.info(
                "No numeric fields were detected for a distribution chart."
            )

    with graph_tabs[1]:

        if len(numeric_cols) >= 2:

            x = st.selectbox(
                "X axis",
                numeric_cols,
                index=0,
                key="batch_x_axis",
            )

            y = st.selectbox(
                "Y axis",
                numeric_cols,
                index=1,
                key="batch_y_axis",
            )

            fig = px.scatter(
                raw,
                x=x,
                y=y,
                title=(
                    f"{x.replace('_', ' ').title()} vs "
                    f"{y.replace('_', ' ').title()}"
                ),
            )

            fig.update_layout(
                margin=dict(
                    l=10,
                    r=10,
                    t=55,
                    b=10,
                )
            )

            show_plotly(
                fig,
                use_container_width=True,
            )

        else:
            st.info(
                "At least two numeric fields are needed."
            )

    with graph_tabs[2]:

        if categorical_cols:

            chosen_cat = st.selectbox(
                "Category",
                categorical_cols,
                key="batch_category_field",
            )

            category_counts = (
                raw[chosen_cat]
                .astype(str)
                .value_counts()
                .head(15)
                .reset_index()
            )

            category_counts.columns = [
                chosen_cat,
                "Customers",
            ]

            fig = px.bar(
                category_counts,
                x=chosen_cat,
                y="Customers",
                title=(
                    f"{chosen_cat.replace('_', ' ').title()} Breakdown"
                ),
            )

            fig.update_layout(
                margin=dict(
                    l=10,
                    r=10,
                    t=55,
                    b=10,
                )
            )

            show_plotly(
                fig,
                use_container_width=True,
            )

        else:
            st.info(
                "No low-cardinality categorical fields were detected."
            )

    # --------------------------------------------------------
    # Analysis table
    # --------------------------------------------------------

    st.markdown("### Analyzed customer data")

    st.markdown(
        '<div class="table-card">',
        unsafe_allow_html=True,
    )

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True,
        height=420,
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    st.download_button(
        "Download Results",
        result.to_csv(index=False),
        "custolens_batch_predictions.csv",
        "text/csv",
        use_container_width=True,
        key="download_batch_results",
    )
