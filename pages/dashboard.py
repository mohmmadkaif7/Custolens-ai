import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split, cross_val_score

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from src.ui import (
    inject_styles,
    page_header,
    load_customer_data,
    money,
    show_plotly,
    segment_counts,
)

from src.prediction_pipeline import model

inject_styles()
df = load_customer_data()

page_header(
    "Intelligence Center",
    "Model Analytics",
    "Explore customer value, segment behavior and trained-model performance from one organized workspace."
)

# ------------------------------------------------------------------
# Shared model evaluation — reproduced from the training workflow.
# ------------------------------------------------------------------
FEATURES = ["age", "income", "purchase_frequency", "annual_spending"]
LABELS = ["Premium", "Regular", "Budget"]

X = df[FEATURES]
y = df["segment"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
y_pred = model.predict(X_test)

test_accuracy = accuracy_score(y_test, y_pred)
precision_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
recall_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)

cv_scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
cv_accuracy = cv_scores.mean()

cv_scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
cv_accuracy = cv_scores.mean()

counts = segment_counts(df)
total = len(df)

# ------------------------------------------------------------------
# Clickable categories
# ------------------------------------------------------------------
tab_overview, tab_customer, tab_model = st.tabs([
    "Overview",
    "Customer Analytics",
    "Model Performance",
])

# ============================== OVERVIEW ===========================
with tab_overview:
    st.markdown('<div class="combined-tab-note">A quick view of the customer base and segment mix.</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, note in [
        (c1, "Total Customers", f"{total:,}", "Training dataset"),
        (c2, "Premium Customers", f"{int(counts['Premium']):,}", f"{counts['Premium']/total*100:.1f}% of total"),
        (c3, "Regular Customers", f"{int(counts['Regular']):,}", f"{counts['Regular']/total*100:.1f}% of total"),
        (c4, "Budget Customers", f"{int(counts['Budget']):,}", f"{counts['Budget']/total*100:.1f}% of total"),
    ]:
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("### Segment distribution")
    left, right = st.columns([0.85, 1.15], gap="large")

    with left:
        pie = px.pie(
            values=counts.values,
            names=counts.index,
            hole=0.62,
            color=counts.index,
            color_discrete_map={
                "Premium": "#7C3AED",
                "Regular": "#2563EB",
                "Budget": "#14B8A6",
            },
        )
        pie.update_traces(textposition="inside", textinfo="percent+label")
        pie.update_layout(
            title="Customer Segment Distribution",
            margin=dict(l=10, r=10, t=50, b=10),
            showlegend=False,
            annotations=[dict(text=f"<b>{total:,}</b><br>Customers", showarrow=False,
                              font=dict(size=16, color="#172033"))],
        )
        show_plotly(pie, use_container_width=True)

    with right:
        fig = px.scatter(
            df,
            x="income",
            y="annual_spending",
            color="segment",
            hover_data=["name", "age", "purchase_frequency"],
            color_discrete_map={
                "Premium": "#7C3AED",
                "Regular": "#2563EB",
                "Budget": "#14B8A6",
            },
            title="Income vs Annual Spending",
        )
        fig.update_layout(
            xaxis_title="Annual Income (₹)",
            yaxis_title="Annual Spending (₹)",
            margin=dict(l=10, r=10, t=55, b=10),
        )
        show_plotly(fig, use_container_width=True)

# ======================== CUSTOMER ANALYTICS =======================
with tab_customer:
    st.markdown('<div class="combined-tab-note">Customer value, purchasing behavior and segment comparison.</div>', unsafe_allow_html=True)

    a, b = st.columns(2, gap="large")
    with a:
        avg_spend = (
            df.groupby("segment", as_index=False)["annual_spending"]
            .mean()
            .rename(columns={"annual_spending": "Average Spending"})
        )
        fig = px.bar(
            avg_spend,
            x="segment",
            y="Average Spending",
            text_auto=".2s",
            color="segment",
            color_discrete_map={
                "Premium": "#7C3AED",
                "Regular": "#2563EB",
                "Budget": "#14B8A6",
            },
            title="Customer Value · Average Spending",
        )
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="₹")
        show_plotly(fig, use_container_width=True)

    with b:
        fig = px.scatter(
            df,
            x="purchase_frequency",
            y="annual_spending",
            color="segment",
            hover_data=["name", "income"],
            color_discrete_map={
                "Premium": "#7C3AED",
                "Regular": "#2563EB",
                "Budget": "#14B8A6",
            },
            title="Purchase Behavior",
        )
        fig.update_layout(
            xaxis_title="Purchase Frequency",
            yaxis_title="Annual Spending (₹)",
        )
        show_plotly(fig, use_container_width=True)

    st.markdown("### Segment comparison")
    summary = (
        df.groupby("segment")
        .agg(
            Customers=("name", "count"),
            Average_Age=("age", "mean"),
            Average_Income=("income", "mean"),
            Average_Spending=("annual_spending", "mean"),
            Average_Frequency=("purchase_frequency", "mean"),
        )
        .reindex(LABELS)
        .reset_index()
    )

    html_rows = []
    for _, row in summary.iterrows():
        html_rows.append(
            f"<tr><td class='segment-name'>{row['segment']}</td>"
            f"<td>{int(row['Customers']):,}</td>"
            f"<td>{row['Average_Age']:.1f}</td>"
            f"<td>{money(row['Average_Income'])}</td>"
            f"<td>{money(row['Average_Spending'])}</td>"
            f"<td>{row['Average_Frequency']:.2f}</td></tr>"
        )

    st.markdown(
        f"""
        <table class="white-table">
          <thead>
            <tr>
              <th>Segment</th><th>Customers</th><th>Average Age</th>
              <th>Average Income</th><th>Average Spending</th><th>Purchase Frequency</th>
            </tr>
          </thead>
          <tbody>{''.join(html_rows)}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Compare segments")
    metric = st.selectbox(
        "Compare metric",
        ["annual_spending", "income", "purchase_frequency", "age"],
        format_func=lambda x: x.replace("_", " ").title(),
    )
    compare = df.groupby("segment", as_index=False)[metric].mean()
    fig = px.bar(
        compare,
        x="segment",
        y=metric,
        color="segment",
        text_auto=".2s",
        color_discrete_map={
            "Premium": "#7C3AED",
            "Regular": "#2563EB",
            "Budget": "#14B8A6",
        },
        title=f"Average {metric.replace('_', ' ').title()} by Segment",
    )
    fig.update_layout(showlegend=False, xaxis_title="")
    show_plotly(fig, use_container_width=True)

# ========================== MODEL PERFORMANCE =====================
with tab_model:
    st.markdown('<div class="combined-tab-note">The trained Random Forest classifier and its validation results.</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    for col, label, value, note in [
        (m1, "Algorithm", "Random Forest", "Classifier"),
        (m2, "Training Samples", f"{len(X_train):,}", "80% of total data"),
        (m3, "Test Accuracy", f"{test_accuracy*100:.1f}%", "20% hold-out test set"),
        (m4, "Cross-Val Accuracy", f"{cv_accuracy*100:.1f}%", "5-fold validation"),
    ]:
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{label}</div>'
                f'<div class="metric-value" style="font-size:1.35rem">{value}</div>'
                f'<div class="metric-note">{note}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("### Model performance")
    left, right = st.columns(2, gap="large")

    with left:
        cm = confusion_matrix(y_test, y_pred, labels=LABELS)
        fig = px.imshow(
            cm,
            x=LABELS,
            y=LABELS,
            text_auto=True,
            color_continuous_scale=["#F5F1FF", "#7C3AED"],
            labels=dict(x="Predicted Segment", y="Actual Segment", color="Customers"),
            title="Confusion Matrix",
        )
        fig.update_layout(
            margin=dict(l=10, r=10, t=55, b=10),
            coloraxis_showscale=False,
        )
        show_plotly(fig, use_container_width=True)

    with right:
        metric_names = ["Accuracy", "Precision (Macro)", "Recall (Macro)", "F1 Score (Macro)"]
        metric_values = [
            test_accuracy * 100,
            precision_macro * 100,
            recall_macro * 100,
            f1_macro * 100,
        ]
        metric_rows = "".join(
            f"<tr><td>{n}</td><td><b>{v:.1f}%</b></td></tr>"
            for n, v in zip(metric_names, metric_values)
        )
        st.markdown(
            f"""
            <div class="model-panel">
              <h4 style="margin-top:0;color:#172033">Performance Metrics</h4>
              <table class="white-table">
                <thead><tr><th>Metric</th><th>Score</th></tr></thead>
                <tbody>{metric_rows}</tbody>
              </table>
              <div style="margin-top:14px;color:#526174;font-size:.84rem">
                The model performs strongly across all three customer segments.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Feature importance")
    importance = pd.DataFrame({
        "Feature": ["Annual Income", "Annual Spending", "Purchase Frequency", "Age"],
        "Importance": model.feature_importances_,
    }).sort_values("Importance", ascending=True)

    fig = px.bar(
        importance,
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        title="Top Features Influencing Predictions",
    )
    fig.update_traces(
        marker_color="#7C3AED",
        texttemplate="%{text:.2f}",
        textposition="outside",
    )
    fig.update_layout(
        xaxis_title="Importance",
        yaxis_title="",
        xaxis_range=[0, max(0.5, importance["Importance"].max() + 0.08)],
        margin=dict(l=10, r=25, t=55, b=10),
    )
    show_plotly(fig, use_container_width=True)

    st.info("Annual income and annual spending are the strongest predictors in the trained Random Forest model.")
