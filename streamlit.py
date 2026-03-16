import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(page_title="Global Seismic Trends Dashboard", layout="wide")

st.title("Global Seismic Trends: Earthquake Insights")


# MYSQL CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Loga2003@",
    database="b115_b118"
)

# LOAD DATA
query = "SELECT * FROM earthquakes"
df = pd.read_sql(query, conn)

# SIDEBAR FILTERS
st.sidebar.header("Filters")

min_mag = st.sidebar.slider(
    "Minimum Magnitude",
    float(df["mag"].min()),
    float(df["mag"].max()),
    float(df["mag"].min())
)

depth_range = st.sidebar.slider(
    "Depth Range (km)",
    float(df["depth_km"].min()),
    float(df["depth_km"].max()),
    (float(df["depth_km"].min()), float(df["depth_km"].max()))
)

filtered_df = df[
    (df["mag"] >= min_mag) &
    (df["depth_km"] >= depth_range[0]) &
    (df["depth_km"] <= depth_range[1])
]

# DATASET OVERVIEW
st.header("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Earthquakes", len(df))
col2.metric("Average Magnitude", round(df["mag"].mean(),2))
col3.metric("Max Magnitude", df["mag"].max())

st.subheader("Full Earthquake Dataset (All 26 Columns)")
st.dataframe(filtered_df, use_container_width=True)

# TOP 10 STRONGEST EARTHQUAKES
st.header("Top 10 Strongest Earthquakes")

top_mag = pd.read_sql(
    "SELECT place, mag, depth_km, time FROM earthquakes ORDER BY mag DESC LIMIT 10",
    conn
)

st.dataframe(top_mag)

# TOP 10 DEEPEST EARTHQUAKES
st.header("Top 10 Deepest Earthquakes")

top_depth = pd.read_sql(
    "SELECT place, depth_km, mag, time FROM earthquakes ORDER BY depth_km DESC LIMIT 10",
    conn
)

st.dataframe(top_depth)

# EARTHQUAKES PER YEAR
st.header("Earthquakes Per Year")

year_data = pd.read_sql("""
SELECT year, COUNT(*) AS total
FROM earthquakes
GROUP BY year
ORDER BY year
""", conn)

fig_year = px.bar(year_data, x="year", y="total", title="Earthquakes per Year")

st.plotly_chart(fig_year, use_container_width=True)

# MAGNITUDE DISTRIBUTION
st.header("Magnitude Distribution")

fig_mag = px.histogram(
    filtered_df,
    x="mag",
    nbins=40,
    title="Magnitude Distribution"
)

st.plotly_chart(fig_mag, use_container_width=True)

# DEPTH VS MAGNITUDE
st.header("Depth vs Magnitude")

fig_scatter = px.scatter(
    filtered_df,
    x="depth_km",
    y="mag",
    hover_data=["place"],
    title="Depth vs Magnitude Relationship"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# TSUNAMI ANALYSIS
st.header("Tsunami Events")

tsunami_data = pd.read_sql("""
SELECT year, COUNT(*) AS tsunami_count
FROM earthquakes
WHERE tsunami = 1
GROUP BY year
ORDER BY year
""", conn)

# Create chart
fig_tsunami = px.line(
    tsunami_data,
    x="year",
    y="tsunami_count",
    title="Tsunami Events Per Year"
)

st.plotly_chart(fig_tsunami, use_container_width=True)

# STATUS ANALYSIS
st.header("Reviewed vs Automatic Events")

status_data = pd.read_sql(
    """
    SELECT status, COUNT(*) as total
    FROM earthquakes
    GROUP BY status
    """,
    conn
)

fig_status = px.pie(
    status_data,
    values="total",
    names="status",
    title="Event Status Distribution"
)

st.plotly_chart(fig_status, use_container_width=True)
