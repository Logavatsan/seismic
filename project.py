import requests
import pandas as pd
from datetime import datetime

#Starting earthquake data project

# API URL
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

all_data = []

# get last 5 years
start_year = datetime.now().year - 5
end_year = datetime.now().year

print("Fetching earthquake data from USGS API...")

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

        if response.status_code != 200:
            print("API request failed")
            continue

        data = response.json()

        for feature in data["features"]:

            properties = feature["properties"]
            geometry = feature["geometry"]["coordinates"]

            record = {
                "id": feature.get("id"),
                "time": properties.get("time"),
                "updated": properties.get("updated"),
                "latitude": geometry[1] if geometry else None,
                "longitude": geometry[0] if geometry else None,
                "depth_km": geometry[2] if geometry else None,
                "mag": properties.get("mag"),
                "magType": properties.get("magType"),
                "place": properties.get("place"),
                "status": properties.get("status"),
                "tsunami": properties.get("tsunami"),
                "sig": properties.get("sig"),
                "net": properties.get("net"),
                "nst": properties.get("nst"),
                "dmin": properties.get("dmin"),
                "rms": properties.get("rms"),
                "gap": properties.get("gap"),
                "magError": properties.get("magError"),
                "depthError": properties.get("depthError"),
                "magNst": properties.get("magNst"),
                "locationSource": properties.get("locationSource"),
                "magSource": properties.get("magSource"),
                "types": properties.get("types"),
                "ids": properties.get("ids"),
                "sources": properties.get("sources"),
                "type": properties.get("type")
            }

            all_data.append(record)

# convert to dataframe
df = pd.DataFrame(all_data)

print("Data fetched successfully")
print("Dataset shape:", df.shape)

print("First 5 rows:")
print(df.head())

# save raw data
df.to_csv("earthquake_raw.csv", index=False)
print("Raw dataset saved")

print("Cleaning dataset...")

# convert time columns
df["time"] = pd.to_datetime(df["time"], unit="ms")
df["updated"] = pd.to_datetime(df["updated"], unit="ms")

# extract country from place column
df["country"] = df["place"].str.extract(r",\s*(.*)")
df["country"] = df["country"].fillna("Unknown")

# numeric columns
numeric_columns = [
    "mag", "depth_km", "nst", "dmin",
    "rms", "gap", "magError", "depthError",
    "magNst", "sig"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df[numeric_columns] = df[numeric_columns].fillna(0)

print("Creating new columns...")

# derived columns
df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day
df["day_of_week"] = df["time"].dt.day_name()

# depth category
def depth_category(depth):

    if depth < 70:
        return "Shallow"

    elif depth < 300:
        return "Intermediate"

    else:
        return "Deep"

df["depth_category"] = df["depth_km"].apply(depth_category)

# strong earthquake flag
df["strong_earthquake"] = df["mag"].apply(
    lambda x: 1 if x >= 6 else 0
)

print("Checking missing values:")
print(df.isnull().sum())

# save cleaned dataset
df.to_csv("earthquake_cleaned.csv", index=False)

print("Cleaned dataset saved successfully")