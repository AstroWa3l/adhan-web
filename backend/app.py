from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from prayer_times import calculate_prayer_times

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL during production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/prayer-times")
def get_prayer_times(latitude: float = 34.48, longitude: float = -118.19, timezone: int = -8, method: str = 'ISNA'):
    prayer_times = calculate_prayer_times(latitude, longitude, timezone, method)
    # Convert datetime.time objects to strings (HH:MM)
    for pt in ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']:
        prayer_times[pt] = prayer_times[pt].strftime("%H:%M")

    return {
        "date": prayer_times["date"].isoformat(),
        "fajr": prayer_times["fajr"],
        "dhuhr": prayer_times["dhuhr"],
        "asr": prayer_times["asr"],
        "maghrib": prayer_times["maghrib"],
        "isha": prayer_times["isha"]
    }
