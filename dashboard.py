
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("propwealthnext_suburb_data.csv")

# Sidebar controls
st.sidebar.header("🏘️ Suburb Selector & Filters")
selected_score = st.sidebar.slider("🎯 Filter by Investor Score", 0, 100, (60, 100))
filtered_df = df[(df["Investor Score"] >= selected_score[0]) & (df["Investor Score"] <= selected_score[1])]

selected_suburb = st.sidebar.selectbox("📍 Choose a Suburb", filtered_df["Suburb"].unique())

# Main Display
st.title("📊 Suburb Investment Intelligence Report")

st.subheader("🏙️ Suburbs Matching Investor Score")
st.dataframe(filtered_df[["Suburb", "Investor Score"]].drop_duplicates().reset_index(drop=True))

if selected_suburb:
    st.subheader(f"📄 Detailed Report for {selected_suburb}")
    row = df[df["Suburb"] == selected_suburb].iloc[0]
    st.markdown(f"""
    **List Price**: N/A  
    **Median**: N/A  
    **Now**: N/A  

    **12m Growth (%)**: {row['12M Growth (%)']}%  
    **10 Year Growth (%)**: {row['10Y Growth (%)']}%  
    **Growth Gap**: {row['Growth Gap']}  
    **Rent Affordability (% of Income)**: {row['Rent Affordability']}  
    **Buy Affordability (Years)**: {row['Buy Affordability']}  
    **Yield**: {row['Yield']}  
    """)

# Map Visualization
st.subheader("🗺️ Map Visualization of Metrics")
metric = st.selectbox("📌 Select a Metric to Map", [
    "12M Growth (%)", "10Y Growth (%)", "Growth Gap", 
    "Rent Affordability", "Buy Affordability", "Yield", "Investor Score"
])

map_fig = px.scatter(
    df,
    x="Buy Affordability",
    y="Rent Affordability",
    size=metric,
    color=metric,
    hover_name="Suburb",
    title=f"{metric} across Suburbs",
    labels={metric: metric}
)
st.plotly_chart(map_fig)
