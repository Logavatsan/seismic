import pandas as pd
import mysql.connector

print("Loading dataset...")

df = pd.read_csv("earthquake_cleaned.csv")

# fix NaN values
df = df.where(pd.notnull(df), None)

print("Total rows:", len(df))

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

print("Inserting data...")

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

for i, row in df.iterrows():

    values = tuple(row)

    cursor.execute(query, values)

conn.commit()

print("Data inserted successfully")

cursor.close()
conn.close()
