import pandas as pd
import mysql.connector

print("Loading dataset...")

df = pd.read_csv("earthquake_cleaned.csv")

print("Total rows:", len(df))

# remove duplicate earthquake ids
df = df.drop_duplicates(subset="id")

print("Rows after removing duplicates:", len(df))

print("Connecting to MySQL...")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Loga2003@",
    database="b115_b118"
)

cursor = conn.cursor()

print("Inserting data into database...")

query = """
INSERT INTO earthquakes
(id, time, updated, latitude, longitude, depth_km, mag, magType,
alert, felt, cdi, mmi, code, place, status, tsunami, sig,
net, nst, dmin, rms, gap, types, ids, sources, type,
year, month, day, depth_category, strong_earthquake)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s)
"""

for i, row in df.iterrows():

    values = (
        row["id"],
        row["time"],
        row["updated"],
        row["latitude"],
        row["longitude"],
        row["depth_km"],
        row["mag"],
        row["magType"],
        row["alert"],
        row["felt"],
        row["cdi"],
        row["mmi"],
        row["code"],
        row["place"],
        row["status"],
        row["tsunami"],
        row["sig"],
        row["net"],
        row["nst"],
        row["dmin"],
        row["rms"],
        row["gap"],
        row["types"],
        row["ids"],
        row["sources"],
        row["type"],
        row["year"],
        row["month"],
        row["day"],
        row["depth_category"],
        row["strong_earthquake"]
    )

    cursor.execute(query, values)

conn.commit()

print("Data inserted successfully!")

cursor.close()
conn.close()
