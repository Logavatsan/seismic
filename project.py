import requests
import pandas as pd
import re 
from datetime import datetime

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

all_records = []

start_year = datetime.now().year - 5
end_year = datetime.now().year

for year in range(start_year, end_year + 1):

    for month in range(1, 13):

        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
            
        print(start_date, "→", end_date)
        
        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": 3
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            for feature in data["features"]:
                prop = feature["properties"]
                geom = feature["geometry"]["coordinates"]
            
                place_str = prop.get("place", "")
                country = ""
                if place_str:
                    match = re.search(r",\s*([^,]+)$", place_str)
                    if match:
                        country = match.group(1).strip()
                    else:
                        country = place_str

                all_records.append({
                    "id": feature.get("id"),
                    "time": pd.to_datetime(prop.get("time"), unit="ms"),
                    "updated": pd.to_datetime(prop.get("updated"), unit="ms"),
                    "latitude": geom[1],
                    "longitude": geom[0],
                    "depth_km": geom[2],
                    "mag": prop.get("mag"),
                    "magType": prop.get("magType"),
                    "place": place_str,
                    "country": country,
                    "status": prop.get("status"),
                    "tsunami": prop.get("tsunami"),
                    "sig": prop.get("sig"),
                    "net": prop.get("net"),
                    "nst": prop.get("nst"),
                    "dmin": prop.get("dmin"),
                    "rms": prop.get("rms"),
                    "gap": prop.get("gap"),
                    "magError": prop.get("magError"),
                    "depthError": prop.get("depthError"),
                    "magNst": prop.get("magNst"),
                    "locationSource": prop.get("locationSource"),
                    "magSource": prop.get("magSource"),
                    "types": prop.get("types"),
                    "ids": prop.get("ids"),
                    "sources": prop.get("sources"),
                    "type": prop.get("type")
                })
        except:
            print("Error fetching data for this month, skipping")

df = pd.DataFrame(all_records)

num_cols = ["mag", "depth_km", "nst", "dmin", "rms", "gap", "sig"]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day_of_week"] = df["time"].dt.day_name()

def get_depth_cat(d):
    if d < 70: return "Shallow"
    if d < 300: return "Intermediate"
    return "Deep"

df["depth_category"] = df["depth_km"].apply(get_depth_cat)

df.to_csv("earthquake_final.csv", index=False)
print("Saved cleaned data to earthquake_final.csv")
