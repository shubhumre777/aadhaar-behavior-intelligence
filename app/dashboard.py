
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page Config 
st.set_page_config(page_title="Aadhaar Behaviour Intelligence", layout="wide")

#  Custom CSS 
st.markdown("""
<style>
body {background-color: #020617;}
.main {background-color: #020617; color: white;}
.title-text {font-size: 42px; font-weight: 900; color: #38bdf8;}
.subtitle {color: #a5f3fc; font-size: 18px;}
.card {background: linear-gradient(135deg,#1e293b,#0f172a); padding: 20px; border-radius: 18px; margin-bottom: 15px;}
.metric-box {background: linear-gradient(135deg,#6366f1,#22c55e,#f59e0b); padding: 20px; border-radius: 15px; color: black; font-weight: 800; text-align: center;}
.small {color:#94a3b8;font-size:12px}
</style>
""", unsafe_allow_html=True)

# Session State 
if "mode" not in st.session_state:
    st.session_state.mode = "intro"
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0


# Paths 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Loading Data
monthly_df = pd.read_csv(os.path.join(OUTPUT_DIR, "monthly_behavior.csv"))
anomalies_df = pd.read_csv(os.path.join(OUTPUT_DIR, "anomalies.csv"))
risk_df = pd.read_csv(os.path.join(OUTPUT_DIR, "district_risk.csv"))
state_risk_df = pd.read_csv(os.path.join(OUTPUT_DIR, "state_risk.csv"))
coords_df = pd.read_csv(os.path.join(OUTPUT_DIR, "state_coordinates.csv"))

# Risk level creation
q85 = risk_df["risk_score"].quantile(0.85)
q60 = risk_df["risk_score"].quantile(0.60)

def classify(score):
    if score >= q85: return "HIGH"
    if score >= q60: return "MEDIUM"
    return "LOW"

risk_df["risk_level"] = risk_df["risk_score"].apply(classify)

map_points_df = state_risk_df.merge(coords_df, on="state", how="left")

# Title 
st.markdown('<div class="title-text">🧠 Aadhaar Behaviour Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered national biometric behavior monitoring system</div>', unsafe_allow_html=True)

# INTRO 
if st.session_state.mode == "intro":
    st.markdown("""
    <div class="card">
    <h2>📌 About</h2>
    This platform detects abnormal Aadhaar biometric behavior, high-risk regions, system stress & migration signals using AI + ML.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h2>🎯 Problem Statement</h2>
    Identify meaningful patterns, anomalies & predictive indicators in Aadhaar updates to support decision-making & system improvement.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h2>⚙ Architecture</h2>
    Data → Cleaning → Feature Engineering → ML (Isolation Forest) → Risk Engine → Geo Intelligence → Decision Support
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Launch Analysis Dashboard"):
        st.session_state.mode = "analysis"
        st.rerun()

# ANALYSIS 
else:
    if st.button("⬅ Back to Overview"):
        st.session_state.mode = "intro"
        st.rerun()

    #  Summary Metrics 
    st.markdown("## 📊 National Summary")
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f'<div class="metric-box">Districts<br>{len(risk_df)}</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-box">Anomalies<br>{len(anomalies_df)}</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-box">High Risk<br>{len(risk_df[risk_df.risk_level=="HIGH"])}</div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-box">States<br>{risk_df.state.nunique()}</div>', unsafe_allow_html=True)

    # Sidebar Filters 
    st.sidebar.header("🔍 Filters")
    months = sorted(anomalies_df.month.unique())
    month = st.sidebar.selectbox("Month", months)
    state = st.sidebar.selectbox("State", ["All"] + sorted(anomalies_df.state.unique()))

    filt = anomalies_df[anomalies_df.month==month]
    if state!="All": filt=filt[filt.state==state]

    # Tabs 
    tab_labels = [
        "📈 Trends",
        "🚨 Anomalies",
        "🗺 Geo Intelligence",
        "🤖 AI Insights",
        "🔮 Future Risk Prediction"
    ]

    tabs = st.tabs(tab_labels)
    current_tab = st.session_state.active_tab


    # Trends finding :
    with tabs[0]:
        st.subheader("Monthly Updates Trend")
        totals = monthly_df.groupby("month")[["demo_total","bio_total"]].sum().reset_index()
        fig = px.line(totals,x="month",y=["demo_total","bio_total"],markers=True)
        st.plotly_chart(fig,use_container_width=True)
        st.caption(f"Rows: {totals.shape[0]} × Cols: {totals.shape[1]}")

        st.subheader("Biometric/Demographic Ratio Trend")
        ratio = monthly_df.groupby("month")["bio_demo_ratio"].mean().reset_index()
        fig2 = px.area(ratio,x="month",y="bio_demo_ratio",color_discrete_sequence=["#22c55e"])
        st.plotly_chart(fig2,use_container_width=True)
        st.caption(f"Rows: {ratio.shape[0]} × Cols: {ratio.shape[1]}")

        st.subheader("Growth Rate of Biometric Updates")
        growth = totals.copy()
        growth["bio_growth_%"] = growth.bio_total.pct_change()*100
        fig3 = px.bar(growth,x="month",y="bio_growth_%",color="bio_growth_%",color_continuous_scale="Turbo")
        st.plotly_chart(fig3,use_container_width=True)
        if st.button("Next → Anomalies"):
            st.session_state.active_tab = 1
            st.rerun()

    # Anomalies displaying :
    with tabs[1]:
        st.subheader("Anomaly Count Over Time")
        at = anomalies_df.groupby("month").size().reset_index(name="count")
        fig = px.bar(at,x="month",y="count",color="count",color_continuous_scale="Reds")
        st.plotly_chart(fig,use_container_width=True)

        st.subheader("Abnormal Districts (Filtered)")
        st.dataframe(filt.sort_values("bio_demo_ratio",ascending=False),use_container_width=True)
        st.caption(f"Rows: {filt.shape[0]} × Cols: {filt.shape[1]}")
        if st.button("Next → Geo Intelligence"):
            st.session_state.active_tab = 2
            st.rerun()

    # Geo Intelligence
    with tabs[2]:
        st.subheader("India Biometric Risk Hotspots")
        fig = px.scatter_geo(map_points_df,lat="lat",lon="lon",size="risk_score",color="risk_score",
                             hover_name="state",color_continuous_scale="Turbo")
        fig.update_geos(
            visible=False,
            lataxis_range=[6,36],
            lonaxis_range=[68,98],
            showcountries=False,
            showland=True,
            landcolor="#0f172a"
        )
        st.plotly_chart(fig,use_container_width=True)

        st.subheader("Top Risky States")
        top_states = state_risk_df.sort_values("risk_score",ascending=False).head(10)
        fig2 = px.bar(top_states,x="risk_score",y="state",orientation="h",color="risk_score")
        st.plotly_chart(fig2,use_container_width=True)
        if st.button("Next → AI Insights"):
            st.session_state.active_tab = 3
            st.rerun()

    # AI Insights
    with tabs[3]:
        st.subheader("District Risk Ranking")
        st.dataframe(risk_df.sort_values("risk_score",ascending=False).head(50),use_container_width=True)
        st.caption(f"Rows: {risk_df.shape[0]} × Cols: {risk_df.shape[1]}")

        st.subheader("AI Recommendations")
        def recommend(row):
            if row.risk_level=="HIGH": return "Increase centers + Audit infrastructure"
            if row.risk_level=="MEDIUM": return "Monitor & prepare resources"
            return "Normal operations"

        rec_df = risk_df.copy()
        rec_df["recommendation"] = rec_df.apply(recommend,axis=1)
        st.dataframe(rec_df[["state","district","risk_level","recommendation"]].head(30),use_container_width=True)

        st.subheader("Download Data")
        st.download_button("Download anomalies.csv",anomalies_df.to_csv(index=False),"anomalies.csv")
        st.download_button("Download district_risk.csv",risk_df.to_csv(index=False),"district_risk.csv")

        if st.button("Next → Future Risk Prediction"):
            st.session_state.active_tab = 4
            st.rerun()

    with tabs[4]:

        st.subheader("🔮 AI-Based Future Risk Prediction Engine")
        st.markdown("This module uses time-series AI to forecast future Aadhaar system stress.")

        horizon = st.slider("Select prediction horizon (months)", 1, 12, 3)

        if st.button("🚀 Generate AI Forecast"):

            with st.spinner("AI is analyzing past trends and predicting future risk..."):


                from prophet import Prophet

                df = monthly_df.copy()
                df["ds"] = pd.to_datetime(df["month"])
                df = df.sort_values("ds")

                #  Biometric forecast
                bio_df = df[["ds", "bio_total"]].rename(columns={"bio_total": "y"})
                model_bio = Prophet()
                model_bio.fit(bio_df)

                future = model_bio.make_future_dataframe(periods=horizon, freq="M")
                forecast_bio = model_bio.predict(future)

                # Demographic forecast 
                demo_df = df[["ds", "demo_total"]].rename(columns={"demo_total": "y"})
                model_demo = Prophet()
                model_demo.fit(demo_df)
                forecast_demo = model_demo.predict(future)

                # Ratio forecast
                ratio_df = df[["ds", "bio_demo_ratio"]].rename(columns={"bio_demo_ratio": "y"})
                model_ratio = Prophet()
                model_ratio.fit(ratio_df)
                forecast_ratio = model_ratio.predict(future)

                # Plots 
                fig1 = px.line(forecast_bio, x="ds", y="yhat", title="Predicted Biometric Updates", markers=True)
                st.plotly_chart(fig1, use_container_width=True)

                fig2 = px.line(forecast_demo, x="ds", y="yhat", title="Predicted Demographic Updates", markers=True)
                st.plotly_chart(fig2, use_container_width=True)

                fig3 = px.area(forecast_ratio, x="ds", y="yhat", title="Predicted Biometric/Demographic Ratio")
                st.plotly_chart(fig3, use_container_width=True)

                # Risk interpretation
                future_ratio = forecast_ratio.tail(horizon)["yhat"].mean()
                current_ratio = df["bio_demo_ratio"].tail(3).mean()

                st.markdown("### 🧠 AI Interpretation")

                if future_ratio > current_ratio * 1.15:
                    st.error(" High risk increase predicted. Infrastructure stress likely.")
                elif future_ratio > current_ratio * 1.05:
                    st.warning(" Moderate risk increase expected. Monitor closely.")
                else:
                    st.success(" System behavior expected to remain stable.")

                # Forecast table 
                forecast_table = pd.DataFrame({
                    "Month": forecast_bio.tail(horizon)["ds"].dt.strftime("%Y-%m"),
                    "Predicted_Biometric": forecast_bio.tail(horizon)["yhat"].round(0),
                    "Predicted_Demographic": forecast_demo.tail(horizon)["yhat"].round(0),
                    "Predicted_Ratio": forecast_ratio.tail(horizon)["yhat"].round(2)
                })

                st.subheader("📊 Forecast Summary Table")
                st.dataframe(forecast_table, use_container_width=True)

                # -------- Explanation section --------
                latest_bio = int(forecast_table["Predicted_Biometric"].iloc[-1])
                latest_demo = int(forecast_table["Predicted_Demographic"].iloc[-1])
                latest_ratio = float(forecast_table["Predicted_Ratio"].iloc[-1])

                st.markdown("## AI Prediction Explanation & Usage")

                st.markdown(f"""
    ### 🤔 What the AI Predicts

    - **Biometric updates:** ~ {latest_bio:,}  
    - **Demographic updates:** ~ {latest_demo:,}  
    - **Bio/Demo ratio:** {latest_ratio}

    This ratio reflects **system stress, re-verification load, or abnormal activity intensity**.
    """)

            st.markdown("""
    ---

    ### -- How this prediction can be used

    - Plan server & biometric infrastructure capacity  
    - Increase centers before congestion  
    - Allocate staff dynamically  
    - Trigger early audits in risky districts  
    - Simulate infrastructure stress  

    ---

    ### -- Why this matters

    Moves system from **reactive** → **proactive governance**

    - Prevent outages  
    - Improve citizen experience  
    - Optimize resource planning  
    - Enable data-driven policy

    ---

    ### -- Model note

    Uses **Prophet time-series AI** trained on historical Aadhaar patterns  
    Learns seasonality + growth + fluctuations automatically.
    """)
