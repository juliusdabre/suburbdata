
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Load data
df = pd.read_excel("Dataa.xlsx", sheet_name="Sheet2")
df.columns = df.columns.str.strip()

# Rename and filter necessary columns
df = df.rename(columns={"Lat": "Latitude", "Long": "Longitude"})
df = df.dropna(subset=["Suburb", "Latitude", "Longitude", "Investor Score (Out Of 100)"]).drop_duplicates()

# Sidebar Filters
st.sidebar.header("🎯 Filter for Investor Research")
score_range = st.sidebar.slider("Investor Score Range", 0, 100, (60, 100))
selected_state = st.sidebar.multiselect("Filter by State", options=df["State"].unique(), default=df["State"].unique())
selected_type = st.sidebar.multiselect("Property Type", options=df["Property\nType"].unique(), default=df["Property\nType"].unique())

# Apply filters
filtered_df = df[
    (df["Investor Score (Out Of 100)"].between(score_range[0], score_range[1])) &
    (df["State"].isin(selected_state)) &
    (df["Property\nType"].isin(selected_type))
]

st.title("🏡 Smart Investor Dashboard")

# Suburb selection
selected_suburb = st.selectbox("📍 Choose a Suburb to View Report", filtered_df["Suburb"].unique())

# Display metrics with real values
if selected_suburb:
    row = filtered_df[filtered_df["Suburb"] == selected_suburb].iloc[0]
    st.markdown(f"""
    ### 📌 Investor Metrics: {selected_suburb}
    <div style='line-height: 2.2; font-size: 18px;'>
    💰 <b>Investor Score</b>: {row['Investor Score (Out Of 100)']}<br>
    📈 <b>10 Year Growth</b>: {row['10 Year Growth']}%<br>
    🔥 <b>Growth Gap Index</b>: {row['Growth Gap Index']}<br>
    💸 <b>Yield</b>: {row['Yield']}%<br>
    🧮 <b>Buy Affordability</b>: {row['Buy Affordability (Years)']} yrs<br>
    📉 <b>Rent Affordability</b>: {row['Rent Affordability (% Of Income)']}%
    </div>
    """, unsafe_allow_html=True)

# Geo Map
st.subheader("🗺️ Suburb Map Based on Investor Score")
map_fig = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    color="Investor Score (Out Of 100)",
    size="Growth Gap Index",
    hover_name="Suburb",
    zoom=4,
    mapbox_style="open-street-map",
    height=500
)
st.plotly_chart(map_fig)

# Heatmap
st.subheader("🔥 Correlation Heatmap of Investment Metrics")
heat_cols = [
    "Investor Score (Out Of 100)", "Growth Gap Index", "10 Year Growth",
    "Yield", "Buy Affordability (Years)", "Rent Affordability (% Of Income)"
]
corr = filtered_df[heat_cols].corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

buf = io.BytesIO()
fig.savefig(buf, format="png")
st.download_button(
    label="📥 Download Heatmap as PNG",
    data=buf.getvalue(),
    file_name="heatmap_investor_metrics.png",
    mime="image/png"
)
