import pandas as pd
import mysql.connector

print("Loading dataset")

df = pd.read_csv("earthquake_final.csv")

# Convert NaN → None safely
df = df.astype(object).where(pd.notnull(df), None)

print("Total rows:", len(df))

# Remove duplicates
df = df.drop_duplicates(subset="id")

print("Rows after removing duplicates:", len(df))

columns = [
    "id","time","updated","latitude","longitude","depth_km","mag","magType",
    "alert","felt","cdi","mmi","code","place","status","tsunami","sig",
    "net","nst","dmin","rms","gap","types","ids","sources","type",
    "year","month","day","depth_category","strong_earthquake"
]

df = df.reindex(columns=columns)

# Fix derived columns if missing
if "day" not in df or df["day"].isnull().all():
    df["day"] = pd.to_datetime(df["time"]).dt.day

if "strong_earthquake" not in df or df["strong_earthquake"].isnull().all():
    df["strong_earthquake"] = df["mag"].apply(lambda x: 1 if x and x >= 6 else 0)

print("Connecting to MySQL")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database=""
)

cursor = conn.cursor()

print("Preparing data")

data = [
    tuple(None if pd.isna(v) else v for v in row)
    for row in df.to_numpy()
]

print("Inserting data")

query = """
INSERT INTO earthquakes
(id,time,updated,latitude,longitude,depth_km,mag,magType,
alert,felt,cdi,mmi,code,place,status,tsunami,sig,
net,nst,dmin,rms,gap,types,ids,sources,type,
year,month,day,depth_category,strong_earthquake)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s,%s,%s,%s,%s,
%s,%s,%s,%s,%s)
"""

try:
    cursor.executemany(query, data)
    conn.commit()
    print("Data inserted successfully")

except Exception as e:
    conn.rollback()
    print("Error:", e)

finally:
    cursor.close()
    conn.close()
    print("Connection closed")
