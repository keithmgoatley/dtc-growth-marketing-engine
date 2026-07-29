import streamlit as st, pandas as pd, numpy as np
import plotly.express as px, plotly.graph_objects as go
import data as D

# ELITE UX CONFIGURATION
st.set_page_config(page_title="DTC Growth Marketing Engine", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: radial-gradient(circle at 50% 0%, #0f172a, #020617); color: #f8fafc; }
h1 { background: linear-gradient(90deg, #10b981, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; letter-spacing: -1px; }
h2, h3 { color: #f8fafc; font-weight: 600; }

/* Glassmorphism Metric Cards */
div[data-testid="metric-container"] {
    background: linear-gradient(145deg, rgba(30,41,59,0.7) 0%, rgba(15,23,42,0.7) 100%);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    border-color: rgba(16,185,129,0.8);
    box-shadow: 0 20px 30px -5px rgba(16,185,129,0.2);
}
[data-testid="stMetricValue"] { font-size: 2.4rem !important; font-weight: 800; color: #f8fafc !important; }
[data-testid="stMetricDelta"] { font-size: 0.85rem !important; }
[data-testid="stMetricLabel"] { color: #34d399 !important; text-transform: uppercase; letter-spacing: 1.2px; font-size: 0.75rem !important; }

/* Advanced Tab Styling */
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: rgba(30,41,59,0.5); padding: 8px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }
.stTabs [data-baseweb="tab"] { color: #94a3b8; padding: 10px 20px; border-radius: 8px; transition: all 0.2s; }
.stTabs [aria-selected="true"] { background: rgba(16,185,129,0.15) !important; color: #34d399 !important; border-bottom: none !important; box-shadow: inset 0 0 0 1px rgba(16,185,129,0.5); }

/* ICE Score Badges */
.ice-card { background: #020617; border: 1px solid #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #10b981; }
</style>
""", unsafe_allow_html=True)

PLOT_BG = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1"))

# LOAD DATA
channel_df = D.get_channel_metrics()
cohort_df = D.get_ltv_cohort_curves()
ice_df = D.get_ice_experiment_roadmap()

# HEADER
st.title("DTC Growth & Unit Economics Command Centre")
st.markdown("<p style='color:#94a3b8; font-size:1.1rem; max-width: 900px; margin-bottom: 2rem;'>Diagnosing DTC growth constraints, modeling LTV:CAC & payback velocity, and orchestrating hypothesis-led experimentation across Meta, Google, Shopify, and Klaviyo data stacks.</p>", unsafe_allow_html=True)

# SIDEBAR SIMULATOR
with st.sidebar:
    st.markdown("<h3 style='color:#34d399;'>Media Allocation Simulator</h3>", unsafe_allow_html=True)
    meta_shift = st.slider("Meta Budget Shift (%)", -30, 30, 0, step=5)
    cro_cvr_lift = st.slider("Target CVR Uplift (%)", 0.0, 25.0, 8.5, step=0.5) / 100
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>Simulates marginal CAC response and revenue impact from CRO velocity.</p>", unsafe_allow_html=True)

# TOP KPI METRICS
c1, c2, c3, c4 = st.columns(4)
blended_cac = (channel_df["Monthly_Spend"].sum() / (channel_df["Monthly_Spend"] / channel_df["Blended_CAC"]).sum())
blended_ltv = channel_df["12M_LTV"].mean()
c1.metric("Blended LTV:CAC Ratio", f"{(blended_ltv / blended_cac):.2f}x", "Target > 3.0x")
c2.metric("Blended CAC", f"£{blended_cac:.2f}", f"{(meta_shift*0.1):+.1f}% Efficiency Shift")
c3.metric("Avg Payback Period", f"{(channel_df['Payback_Months'].mean()):.1f} Months", "Capital Efficient")
c4.metric("Blended MER (Media Eff. Ratio)", f"{((channel_df['Monthly_Spend'].sum() / (channel_df['Monthly_Spend'] * channel_df['ROAS']).sum()))*100:.1f}%", "Top Quartile DTC")

# TABS
t1, t2, t3 = st.tabs(["Unit Economics & LTV Cohorts", "Channel Efficiency & Spend Allocation", "Hypothesis-Led ICE Experimentation Roadmap"])

with t1:
    st.markdown("### 12-Month Cohort LTV Progression & Retention Curves")
    st.markdown("<p style='color:#94a3b8;'>Tracking cumulative customer LTV over time to validate payback speed and repeat purchase health.</p>", unsafe_allow_html=True)
    
    fig_ltv = go.Figure()
    colors = ["#34d399", "#06b6d4", "#3b82f6", "#818cf8", "#a855f7", "#ec4899"]
    for i, col in enumerate(cohort_df.index):
        fig_ltv.add_trace(go.Scatter(x=cohort_df.columns, y=cohort_df.loc[col], mode='lines+markers', name=col, line=dict(color=colors[i % len(colors)], width=3)))
    
    fig_ltv.update_layout(**PLOT_BG, height=380, xaxis_title="Months Post Initial Purchase", yaxis_title="Cumulative LTV (£)", margin=dict(t=20, b=20, l=10, r=10))
    st.plotly_chart(fig_ltv, use_container_width=True)

with t2:
    st.markdown("### Channel Efficiency, Payback & MER Breakdown")
    st.dataframe(
        channel_df.style.format({"Monthly_Spend": "£{:,.0f}", "Blended_CAC": "£{:.2f}", "AOV": "£{:.2f}", "12M_LTV": "£{:.2f}", "ROAS": "{:.2f}x", "Payback_Months": "{:.1f} Mo", "LTV_CAC_Ratio": "{:.2f}x"})
        .background_gradient(subset=['LTV_CAC_Ratio'], cmap='Greens'),
        use_container_width=True, hide_index=True, height=220
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Monthly Spend vs ROAS by Channel")
        fig_bubble = px.scatter(channel_df, x="Monthly_Spend", y="ROAS", size="12M_LTV", color="Channel",
                                hover_name="Channel", size_max=40, color_discrete_sequence=["#34d399", "#06b6d4", "#a855f7", "#fbbf24", "#3b82f6"])
        fig_bubble.update_layout(**PLOT_BG, height=300, margin=dict(t=20, b=10, l=10, r=10))
        st.plotly_chart(fig_bubble, use_container_width=True)
    with col2:
        st.markdown("#### CAC vs Payback Velocity (Months)")
        fig_payback = px.bar(channel_df, x="Channel", y="Payback_Months", color="Channel", color_discrete_sequence=["#34d399", "#06b6d4", "#a855f7", "#fbbf24", "#3b82f6"])
        fig_payback.update_layout(**PLOT_BG, height=300, margin=dict(t=20, b=10, l=10, r=10), showlegend=False)
        st.plotly_chart(fig_payback, use_container_width=True)

with t3:
    st.markdown("### ICE Prioritised Experimentation Matrix")
    st.markdown("<p style='color:#94a3b8;'>Structured roadmap testing hypotheses across Acquisition, CRO, and Retention to eliminate growth bottlenecks.</p>", unsafe_allow_html=True)
    
    st.dataframe(
        ice_df.style.format({"ICE_Score": "{:.1f}"})
        .background_gradient(subset=['ICE_Score'], cmap='Greens')
        .map(lambda v: "color:#34d399" if "Completed" in str(v) else ("color:#fbbf24" if "Active" in str(v) or "Testing" in str(v) else "color:#94a3b8"), subset=["Status"]),
        use_container_width=True, hide_index=True, height=250
    )
