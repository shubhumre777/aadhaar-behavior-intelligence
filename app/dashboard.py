import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.set_page_config(page_title="Aadhaar Behaviour Intelligence", layout="wide")

st.title("🧠 Aadhaar Biometric Behaviour Intelligence System")

# Load data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

monthly_df = pd.read_csv(os.path.join(OUTPUT_DIR, "monthly_behavior.csv"))
anomalies_df = pd.read_csv(os.path.join(OUTPUT_DIR, "anomalies.csv"))
risk_df = pd.read_csv(os.path.join(OUTPUT_DIR, "district_risk.csv"))
state_risk_df = pd.read_csv(os.path.join(OUTPUT_DIR, "state_risk.csv"))
coords_df = pd.read_csv(os.path.join(OUTPUT_DIR, "state_coordinates.csv"))

map_points_df = state_risk_df.merge(coords_df, on="state", how="left")


st.success("Data loaded successfully")

# Sidebar filters

st.sidebar.header("Filters") # name showing at the slidebar .

# in slidebar month filter will be visible .

all_months = sorted(anomalies_df['month'].unique())
selected_month = st.sidebar.selectbox("Select Month", ["All"] + all_months)

all_states = sorted(anomalies_df['state'].unique())
selected_state = st.sidebar.selectbox("Select State", ["All"] + all_states)

filtered_anomalies = anomalies_df.copy()

if selected_month != "All":
    filtered_anomalies = filtered_anomalies[filtered_anomalies['month'] == selected_month]

if selected_state != "All":
    filtered_anomalies = filtered_anomalies[filtered_anomalies['state'] == selected_state]


# Section 1: Monthly trend (India)

st.header("📈 Monthly Update Trends (India)")

monthly_totals = (
    monthly_df
    .groupby('month')[[
        'demo_age_5_17','demo_age_17_',
        'bio_age_5_17','bio_age_17_'
    ]]
    .sum()
)

st.line_chart(monthly_totals)

# Section 2: Anomaly trend

st.header("🚨 Anomaly Trend Over Time")

anomaly_counts = anomalies_df.groupby('month').size()

fig, ax = plt.subplots(figsize=(10,4))
anomaly_counts.plot(kind='bar', ax=ax)
ax.set_title("Number of abnormal districts per month")
ax.set_xlabel("Month")
ax.set_ylabel("Count")

st.pyplot(fig)


# Abnormal districts table

st.header("📍 Abnormal Districts (Filtered)")

display_cols = ['month','state','district','bio_total','demo_total','bio_demo_ratio']

table_df = filtered_anomalies[display_cols].sort_values('bio_demo_ratio', ascending=False)
table_df['bio_demo_ratio'] = table_df['bio_demo_ratio'].round(2)

st.dataframe(table_df, use_container_width=True)


# Risk ranking

st.header("⚠️ District Risk Ranking (Overall)")

risk_view = risk_df.sort_values('risk_score', ascending=False).copy()
risk_view['risk_score'] = risk_view['risk_score'].round(2)

st.dataframe(risk_view.head(50), use_container_width=True)


st.header("📍 Biometric Risk Hotspots (Point Map)")

fig = px.scatter_geo(
    map_points_df,
    lat="lat",
    lon="lon",
    size="risk_score",
    color="risk_score",
    hover_name="state",
    size_max=40,
    projection="natural earth",
    title="Aadhaar Biometric Risk Hotspots (State Level)",
    color_continuous_scale="Reds"
)

fig.update_geos(
    fitbounds="locations",
    visible=True,
    showcountries=True,
    countrycolor="Black"
)

st.plotly_chart(fig, use_container_width=True)


