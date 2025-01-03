from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime, date
from prayer_times import calculate_prayer_times, prayTimes
import os
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL during production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Geoapify API Key (replace with your actual key)
# Load environment variables from .env file
load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

@app.get("/")
def get_prayer_times(city: str, country: str, state: str = None, method: str = "ISNA"):
    print(f"Received query parameters: city={city}, state={state}, country={country}, method={method}")

    # Construct the Geoapify query
    query = f"{city},{country}"
    if state:
        query = f"{city},{state},{country}"

    geoapify_url = f"https://api.geoapify.com/v1/geocode/search?text={query}&format=json&apiKey={GEOAPIFY_API_KEY}"
    response = requests.get(geoapify_url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch location data.")
    data = response.json()
    print("Geoapify API response:", data)

    # Process results
    results = data.get("results", [])
    if not results:
        raise HTTPException(status_code=404, detail="Location not found.")

    # Filter results by state if provided
    filtered_results = [
        result for result in results
        if state and result.get("state_code", "").lower() == state.lower()
    ]

    # Use the first filtered result if available, otherwise default to the first result
    location = filtered_results[0] if filtered_results else results[0]

    # Extract latitude, longitude, and timezone
    latitude = location["lat"]
    longitude = location["lon"]
    timezone_offset = location.get("timezone", {}).get("offset_STD_seconds")
    if timezone_offset is None:
        raise HTTPException(status_code=500, detail="Timezone information is missing for the location.")
    timezone_offset //= 3600  # Convert seconds to hours

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
