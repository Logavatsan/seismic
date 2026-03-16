import pandas as pd
from sqlalchemy import create_engine

print("Loading dataset...")

df = pd.read_csv("earthquake_cleaned.csv")

print("Total rows:", len(df))

# remove duplicate earthquake ids
df = df.drop_duplicates(subset="id")

print("Rows after removing duplicates:", len(df))

print("Connecting to MySQL...")

engine = create_engine(
    "mysql+pymysql://root:Loga2003%40@localhost/b115_b118"
)

print("Inserting data...")

df.to_sql(
    "earthquakes",
    engine,
    if_exists="replace",
    index=False,
    chunksize=1000
)

print("Data inserted successfully!")