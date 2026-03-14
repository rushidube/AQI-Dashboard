import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="AQI Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("data/city_day.csv")

# Convert Date column to datetime FIRST
df["Date"] = pd.to_datetime(df["Date"])

# Create Year and Month columns
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()

# SIDEBAR FILTERS 
st.sidebar.header("Filters")

# City Dropdown
selected_city = st.sidebar.selectbox(
    "Select City",
    ["All Cities"] + sorted(df["City"].dropna().unique())
)

# Year Dropdown
selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All Years"] + sorted(df["Year"].unique())
)

# Apply Filters
filtered_df = df

if selected_city != "All Cities":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_year != "All Years":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

# SIDEBAR INFO
st.sidebar.title("About This Project")

st.sidebar.markdown("""
### AQI Data Analytics Dashboard

This dashboard analyzes **Air Quality Index (AQI)** data across major Indian cities.

### Technologies Used
- Python
- Pandas
- Plotly
- Streamlit

### Dataset
Indian Air Quality Dataset

### Author
Rushikesh Dube
""")

st.sidebar.markdown("### Key Insights")

st.sidebar.write("""
• Delhi shows consistently higher AQI levels  
• PM2.5 strongly correlates with AQI  
• Pollution peaks during winter months
""")

#  MAIN DASHBOARD

st.title("Air Quality Index (AQI) Analysis Dashboard")

st.subheader(f"Viewing Data: {selected_city} | {selected_year}")

# KPI Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_df))
col2.metric("Cities Covered", filtered_df["City"].nunique())
col3.metric("Average AQI", round(filtered_df["AQI"].mean(), 2))

st.write("""
This dashboard analyzes Air Quality Index (AQI) data across major Indian cities.  
It provides insights into pollution trends, city comparisons, and seasonal patterns.
""")

# AQI TREND

aqi_trend = filtered_df.groupby("Date")["AQI"].mean().reset_index()

fig1 = px.line(
    aqi_trend,
    x="Date",
    y="AQI",
    title="AQI Trend Over Time" if selected_city == "All Cities" else f"AQI Trend for {selected_city}"
)

st.plotly_chart(fig1, use_container_width=True)

# TOP POLLUTED CITIES

city_aqi = filtered_df.groupby("City")["AQI"].mean().reset_index()
city_aqi = city_aqi.sort_values(by="AQI", ascending=False).head(10)

fig2 = px.bar(
    city_aqi,
    x="City",
    y="AQI",
    title="Top 10 Most Polluted Cities",
    color="AQI"
)

st.plotly_chart(fig2, use_container_width=True)

# MONTHLY AQI TREND

monthly_aqi = filtered_df.groupby("Month")["AQI"].mean().reset_index()

fig3 = px.line(
    monthly_aqi,
    x="Month",
    y="AQI",
    title="Average AQI by Month",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)


