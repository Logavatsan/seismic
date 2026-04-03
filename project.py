import requests
import pandas as pd
from datetime import datetime

print("Starting earthquake data project")

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

all_records = []

start_year = datetime.now().year - 5
end_year = datetime.now().year

print("Fetching earthquake data from USGS API")

for year in range(start_year, end_year + 1):

    for month in range(1, 13):

        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"

        print("Fetching:", start_date, "to", end_date)

        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": 3
        }

        response = requests.get(url, params=params)

        data = response.json()

        for f in data["features"]:

            p = f["properties"]
            g = f["geometry"]["coordinates"]

            all_records.append({

                "id": f.get("id"),

                "time": pd.to_datetime(p.get("time"), unit="ms"),
                "updated": pd.to_datetime(p.get("updated"), unit="ms"),

                "latitude": g[1] if g else None,
                "longitude": g[0] if g else None,
                "depth_km": g[2] if g else None,

                "mag": p.get("mag"),
                "magType": p.get("magType"),

                "alert": p.get("alert"),
                "felt": p.get("felt"),
                "cdi": p.get("cdi"),
                "mmi": p.get("mmi"),
                "code": p.get("code"),

                "place": p.get("place"),
                "status": p.get("status"),
                "tsunami": p.get("tsunami"),
                "sig": p.get("sig"),

                "net": p.get("net"),
                "nst": p.get("nst"),
                "dmin": p.get("dmin"),
                "rms": p.get("rms"),
                "gap": p.get("gap"),

                "types": p.get("types"),
                "ids": p.get("ids"),
                "sources": p.get("sources"),
                "type": p.get("type")
            })

print("Data collection finished")

df = pd.DataFrame(all_records)

print("Total records:", len(df))

df.to_csv("earthquake_raw.csv", index=False)

print("Raw dataset saved")
print("Cleaning dataset")

numeric_cols = [
    "mag", "depth_km", "felt", "cdi",
    "mmi", "sig", "nst", "dmin",
    "rms", "gap"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df[numeric_cols] = df[numeric_cols].fillna(0)

df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day

def depth_category(depth):

    if depth < 70:
        return "Shallow"

    elif depth < 300:
        return "Intermediate"

    else:
        return "Deep"

df["depth_category"] = df["depth_km"].apply(depth_category)

strong_earthquake = []

for x in df["mag"]:
    if x >= 6:
        strong_earthquake.append(1)
    else:
        strong_earthquake.append(0)

df["strong_earthquake"] = strong_earthquake

print("Checking missing values:")
print(df.isnull().sum())

df.to_csv("earthquake_cleaned.csv", index=False)

print("Cleaned dataset saved successfully")
print("Project completed")
