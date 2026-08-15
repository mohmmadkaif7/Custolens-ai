import streamlit as st
from src.ui import inject_styles, load_recommendation_data

inject_styles()
df = load_recommendation_data()

st.markdown('<div class="page-kicker">Action Center</div>', unsafe_allow_html=True)
st.title("Business Strategies")
st.markdown('<div class="page-subtitle">Turn customer segments into focused retention, growth and engagement actions.</div>', unsafe_allow_html=True)

segment_cols = st.columns(3, gap="small")
for i, segment in enumerate(["Premium", "Regular", "Budget"]):
    seg = df[df["segment"] == segment]
    if seg.empty:
        continue
    row = seg.iloc[0]
    actions = [x.strip() for x in str(row["recommendations"]).split(".") if x.strip()]
    with segment_cols[i]:
        st.markdown(f"""
        <div class="strategy-card strategy-card-equal">
          <span class="strategy-badge">{segment.upper()}</span>
          <div class="strategy-title">{row["strategy"]}</div>
          <div class="strategy-goal"><b>Business goal</b><br>{row["business_goal"]}</div>
          <hr>
          <div class="reason-title">Recommended actions</div>
          <ul class="strategy-list">
            {''.join(f'<li>{a}.</li>' for a in actions)}
          </ul>
        </div>
        """, unsafe_allow_html=True)
