import requests
import datetime
import pytz
import streamlit as st

# Function to get current weather data from Open-Meteo
def get_current_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=sunrise,sunset&timezone=auto"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Coordinates for Tuscaloosa
lat = 33.2090
lon = -87.5692

# Timezone for Tuscaloosa
local_timezone = pytz.timezone('America/Chicago')

# Fetch weather data
weather_data = get_current_weather(lat, lon)
if weather_data:
    # Get the raw sunrise and sunset times from the API (assume these times are already in local time)
    sunrise_local_str = weather_data['daily']['sunrise'][0]
    sunset_local_str = weather_data['daily']['sunset'][0]

    # Parse the string times as naive datetime objects (they are already in local time)
    sunrise_naive = datetime.datetime.strptime(sunrise_local_str, '%Y-%m-%dT%H:%M')
    sunset_naive = datetime.datetime.strptime(sunset_local_str, '%Y-%m-%dT%H:%M')

    # Localize these naive datetime objects to the local timezone
    sunrise_local = local_timezone.localize(sunrise_naive)
    sunset_local = local_timezone.localize(sunset_naive)

    # Debugging outputs for checking times
    st.write(f"Sunrise in local time (before formatting): {sunrise_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    st.write(f"Sunset in local time (before formatting): {sunset_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")

    # Format for display
    sunrise_local_str = sunrise_local.strftime('%H:%M')
    sunset_local_str = sunset_local.strftime('%H:%M')

    # Display current local time in Tuscaloosa using datetime.now()
    local_time = datetime.datetime.now(local_timezone).strftime('%H:%M')

    # Display results
    st.write(f"Sunrise in local time: {sunrise_local_str}")
    st.write(f"Sunset in local time: {sunset_local_str}")
    st.write(f"Local Time in Tuscaloosa: {local_time}")
else:
    st.write("Failed to fetch weather data")
