import os
import requests
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIG ---
CITY_LAT = 44.0266   # Ontario, OR
CITY_LON = -116.9629
SHEET_NAME = "Payette Weather Log"

# --- WEATHER API ---
api_key = os.environ["OPENWEATHER_API_KEY"]
url = (
    "https://api.openweathermap.org/data/2.5/weather"
    f"?lat={CITY_LAT}&lon={CITY_LON}&appid={api_key}&units=imperial"
)

data = requests.get(url).json()

# --- PARSE WEATHER ---
temp = data["main"]["temp"]
pressure = data["main"]["pressure"]
wind_speed = data["wind"].get("speed", "")
wind_dir = data["wind"].get("deg", "")
clouds = data["clouds"]["all"]
cloud_type = data["weather"][0]["description"]
precip = data.get("rain", {}).get("1h", 0)

now = datetime.now()
date = now.strftime("%Y-%m-%d")
time = now.strftime("%I:%M %p")

# --- GOOGLE SHEETS ---
creds_json = os.environ["GOOGLE_CREDS"]
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(
    eval(creds_json), scopes=scopes
)

client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

sheet.append_row([
    date,
    time,
    temp,
    pressure,
    wind_speed,
    wind_dir,
    precip,
    cloud_type,
    clouds
])
