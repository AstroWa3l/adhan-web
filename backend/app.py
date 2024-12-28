from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime, date
from prayer_times import calculate_prayer_times, prayTimes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL during production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Geoapify API Key (replace with your actual key)
GEOAPIFY_API_KEY = "8c2ef5ff4e55494a99a719955bc092af"

@app.get("/prayer-times")
def get_prayer_times(
    city: str = None,
    country: str = None,
    latitude: float = None,
    longitude: float = None,
    method: str = "ISNA"
):
    if city and country:
        # Fetch coordinates and timezone from Geoapify API
        geoapify_url = f"https://api.geoapify.com/v1/geocode/search?text={city},{country}&format=json&apiKey={GEOAPIFY_API_KEY}"
        response = requests.get(geoapify_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch location data.")
        data = response.json()

        # Check if results are available
        if "results" not in data or len(data["results"]) == 0:
            raise HTTPException(status_code=404, detail="Location not found.")
        location = data["results"][0]
        latitude = location["lat"]
        longitude = location["lon"]
        timezone_offset = location["timezone"]["offset_STD_seconds"] // 3600  # Convert seconds to hours

    elif latitude is not None and longitude is not None:
        # Handle case where latitude and longitude are directly provided
        timezone_offset = -8  # Default to Pacific Time if timezone not available
    else:
        raise HTTPException(
            status_code=400,
            detail="Either city and country or latitude and longitude must be provided."
        )

    # Validate the method
    if method not in prayTimes.methods.keys():
        raise HTTPException(
            status_code=400,
            detail=f"Invalid method. Available methods are: {', '.join(prayTimes.methods.keys())}."
        )

    # Calculate prayer times
    prayer_times = calculate_prayer_times(latitude, longitude, timezone_offset, method)

    # Convert datetime.time objects to strings (HH:MM)
    for pt in ["fajr", "dhuhr", "asr", "maghrib", "isha"]:
        prayer_times[pt] = prayer_times[pt].strftime("%H:%M")

    return {
        "date": prayer_times["date"].isoformat(),
        "fajr": prayer_times["fajr"],
        "dhuhr": prayer_times["dhuhr"],
        "asr": prayer_times["asr"],
        "maghrib": prayer_times["maghrib"],
        "isha": prayer_times["isha"],
    }
