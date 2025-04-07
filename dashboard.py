
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("propwealthnext_suburb_data.csv")

# Sidebar
st.sidebar.header("🏘️ Suburb Selector & Filters")
score_range = st.sidebar.slider("🎯 Filter by Investor Score", 0, 100, (60, 100))
filtered_df = df[(df["Investor Score"] >= score_range[0]) & (df["Investor Score"] <= score_range[1])]
selected_suburb = st.sidebar.selectbox("📍 Choose a Suburb", filtered_df["Suburb"].unique())

# Main title
st.title("📊 Suburb Investment Dashboard")

# Metric display
if selected_suburb:
    row = df[df["Suburb"] == selected_suburb].iloc[0]
    st.markdown(f"""
    ### 📍 Report for **{selected_suburb}**
    <div style='line-height: 2.5; font-size: 18px;'>
    💰 <b>Median Price</b>: ${int(row['Median Price']) if 'Median Price' in row else 'N/A'}<br>
    📈 <b>12M Growth</b>: {row['12M Growth (%)']}%<br>
    💸 <b>Yield</b>: {row['Yield']}%<br>
    📊 <b>Rent Change</b>: N/A<br>
    🧮 <b>Buy Affordability</b>: {row['Buy Affordability']} yrs<br>
    📉 <b>Rent Affordability</b>: {row['Rent Affordability']}%<br>
    📈 <b>10Y Growth (PA)</b>: {row['10Y Growth (%)']}%
    </div>
    """, unsafe_allow_html=True)

# Display map like your screenshot
st.subheader(f"📌 Metric Map: 12M Growth (%) Across All Suburbs")

# Use lat/lon if available or random placeholder
df['Latitude'] = df['Latitude'] if 'Latitude' in df.columns else -33.87
df['Longitude'] = df['Longitude'] if 'Longitude' in df.columns else 151.21

map_fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color="12M Growth (%)",
    size="12M Growth (%)",
    hover_name="Suburb",
    zoom=4,
    height=600,
    mapbox_style="carto-positron",
    color_continuous_scale="Viridis"
)
st.plotly_chart(map_fig)
