import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.title("Global Seismic Trends Dashboard")

print("Connecting to MySQL...")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Loga2003@",
    database="b115_b118"
)

query = "SELECT * FROM earthquakes"

df = pd.read_sql(query, conn)

st.header("Dataset Overview")

st.write("Total earthquakes:", len(df))
st.write("Average magnitude:", round(df["mag"].mean(),2))
st.write("Maximum magnitude:", df["mag"].max())

st.subheader("Earthquake Dataset")

st.dataframe(df)

# Earthquakes per year
st.header("Earthquakes per Year")

year_data = pd.read_sql("""
SELECT year, COUNT(*) as total
FROM earthquakes
GROUP BY year
ORDER BY year
""", conn)

fig1 = px.bar(year_data, x="year", y="total")

st.plotly_chart(fig1)

# Magnitude distribution
st.header("Magnitude Distribution")

fig2 = px.histogram(df, x="mag", nbins=40)

st.plotly_chart(fig2)

# Depth vs magnitude
st.header("Depth vs Magnitude")

fig3 = px.scatter(df, x="depth_km", y="mag")

st.plotly_chart(fig3)

# Strong earthquakes
st.header("Strong Earthquakes")

strong_eq = pd.read_sql("""
SELECT place, mag, depth_km, time
FROM earthquakes
WHERE mag >= 6
ORDER BY mag DESC
LIMIT 10
""", conn)

st.dataframe(strong_eq)

conn.close()
