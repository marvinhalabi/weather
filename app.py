import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import datetime
from streamlit_searchbox import st_searchbox
from time import sleep
from weather_utils import weather_description, weather_emoji
from dotenv import load_dotenv
import os
import pytz
from timezonefinder import TimezoneFinder
from streamlit_extras.stylable_container import stylable_container
import io

# Load environment variables
load_dotenv()

# Load the CSV file
city_data = pd.read_csv('worldcities.csv')

# Streamlit app layout
st.set_page_config(page_title="Weather App", layout="centered", page_icon=":sun_with_face:")
st.header("Weather App :sun_with_face:", divider="rainbow")
st.write("Get the current weather and news for any city.")

# Function to get current weather data from Open-Meteo
def get_current_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=sunrise,sunset&hourly=temperature_2m&timezone=auto"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to filter city suggestions from the CSV file
def get_city_suggestions(query):
    if not query:
        return []
    sleep(0.3)
    results = city_data[city_data['city'].str.contains(query, case=False, na=False)]
    return [result['city'] for result in results[['city']].drop_duplicates().head(10).to_dict(orient='records')]

# Function to get news articles from newsdata.io
def get_news(city_name, country_code):
    api_key = os.getenv('NEWS_API_KEY')
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={city_name}&country={country_code}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Input for city name with autocomplete using streamlit-searchbox
selected_city = st_searchbox(
    search_function=get_city_suggestions,
    label="Enter city name:",
    key="city_searchbox"
)

# Fetch and display weather data if a city is selected
if selected_city:
    city_info = city_data[city_data['city'] == selected_city].iloc[0]
    city_name = city_info['city']
    lat = city_info['lat']
    lon = city_info['lng']
    country_code = city_info['iso2'].lower()

    # Determine the local time zone for the selected city using TimezoneFinder
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=lon, lat=lat)
    
    if timezone_str is None:
        st.error("Could not determine the timezone for the selected city.")
    else:
        # Convert sunrise and sunset times from local time provided by API
        city_timezone = pytz.timezone(timezone_str)
        
        with st.spinner('Fetching weather data...'):
            weather_data = get_current_weather(lat, lon)
        
        if weather_data:
            current_weather = weather_data['current_weather']
            temperature = current_weather['temperature']
            windspeed = current_weather['windspeed']

            # Get sunrise and sunset times in local time (assumed to be provided in local time)
            sunrise_str = weather_data['daily']['sunrise'][0]
            sunset_str = weather_data['daily']['sunset'][0]

            # Parse the sunrise and sunset times
            sunrise_naive = datetime.datetime.strptime(sunrise_str, '%Y-%m-%dT%H:%M')
            sunset_naive = datetime.datetime.strptime(sunset_str, '%Y-%m-%dT%H:%M')

            # Localize the naive times to the city's timezone
            sunrise_local = city_timezone.localize(sunrise_naive)
            sunset_local = city_timezone.localize(sunset_naive)

            # Format the times for display
            sunrise_local_str = sunrise_local.strftime('%H:%M')
            sunset_local_str = sunset_local.strftime('%H:%M')

            # Display local time in the selected city
            local_time = datetime.datetime.now(city_timezone).strftime('%H:%M')

            # Fetch weather code and description
            weather_code = current_weather['weathercode']
            description = weather_description(weather_code)
            weather_emoji_icon = weather_emoji(description, temperature)

            # Use Markdown to increase text size and format weather info
            st.header(f" Current Weather in {city_name} {weather_emoji_icon}")
            st.markdown(f"**🌡️ Temperature:** :blue-background[{temperature}°C]")
            st.markdown(f"**☁️ Weather Description:** :blue-background[{description}]")
            st.markdown(f"**💨 Wind Speed:** :blue-background[{windspeed} m/s]")
            st.markdown(f"**☀️ Sunrise:** :blue-background[{sunrise_local_str}]")
            st.markdown(f"**🌑 Sunset:** :blue-background[{sunset_local_str}]")
            st.markdown(f"**🕒 Local Time:** :blue-background[{local_time}]")


            # Check if 'hourly' data is available before attempting to access it
            if 'hourly' in weather_data:
                hourly = weather_data['hourly']
                times = [datetime.datetime.fromisoformat(t).astimezone(city_timezone).strftime('%H:%M') for t in hourly['time'][:24]]
                temps = hourly['temperature_2m'][:24]

                forecast_df = pd.DataFrame({'Time': times, 'Temperature': temps})
                plt.figure(figsize=(10, 4))  # Increased size of the plot
                plt.plot(forecast_df['Time'], forecast_df['Temperature'], marker='o')
                plt.title('Hourly Temperature Forecast')
                plt.xlabel('Time')
                plt.ylabel('Temperature (°C)')
                plt.xticks(rotation=45)

                # Save the plot to a BytesIO object
                buf = io.BytesIO()
                plt.savefig(buf, format="png", bbox_inches='tight')  # Use bbox_inches to avoid cutoff
                buf.seek(0)

                # Display the plot with a border and rounded corners using stylable_container
                with stylable_container(
                    key="container_with_border",
                    css_styles="""
                        {
                            border-radius: 15px;
                            padding: 10px;
                            background-color: white;
                            overflow: hidden;
                        }
                    """,
                ):
                    st.image(buf, use_column_width=True)
            else:
                st.write("Hourly forecast data is not available.")

        with st.spinner('Fetching news articles...'):
            news_data = get_news(city_name, country_code)
        
        if news_data and 'results' in news_data:
            st.header(f"Latest News in {city_name}", divider="red")
            for article in news_data['results'][:3]:
                st.write(f"### {article['title']}")
                st.write(f"{article['description']}")
                st.write(f"[Read more]({article['link']})")
        else:
            st.error("Failed to retrieve news articles. Please try again.")
