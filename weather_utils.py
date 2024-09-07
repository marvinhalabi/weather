# weather_utils.py

def weather_description(weather_code):
    weather_descriptions = {
        0: "clear",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "fog",
        48: "depositing rime fog",
        51: "light drizzle",
        53: "moderate drizzle",
        55: "dense drizzle",
        56: "light freezing drizzle",
        57: "dense freezing drizzle",
        61: "slight rain",
        63: "moderate rain",
        65: "heavy rain",
        66: "light freezing rain",
        67: "heavy freezing rain",
        71: "slight snow fall",
        73: "moderate snow fall",
        75: "heavy snow fall",
        77: "snow grains",
        80: "slight rain showers",
        81: "moderate rain showers",
        82: "violent rain showers",
        85: "slight snow showers",
        86: "heavy snow showers",
        95: "thunderstorm",
        96: "thunderstorm with slight hail",
        99: "thunderstorm with heavy hail"
    }
    return weather_descriptions.get(weather_code, "unknown")

def weather_emoji(description, temperature):
    weather_emojis = {
        "clear": ":sunny:",
        "mainly clear": ":sunny:",
        "partly cloudy": ":partly_sunny:",
        "overcast": ":cloud:",
        "fog": ":fog:",
        "depositing rime fog": ":fog:",
        "light drizzle": ":rain_cloud:",
        "moderate drizzle": ":rain_cloud:",
        "dense drizzle": ":rain_cloud:",
        "light freezing drizzle": ":rain_cloud:",
        "dense freezing drizzle": ":rain_cloud:",
        "slight rain": ":rain_cloud:",
        "moderate rain": ":rain_cloud:",
        "heavy rain": ":rain_cloud:",
        "light freezing rain": ":rain_cloud:",
        "heavy freezing rain": ":rain_cloud:",
        "slight snow fall": ":snowflake:",
        "moderate snow fall": ":snowflake:",
        "heavy snow fall": ":snowflake:",
        "snow grains": ":snowflake:",
        "slight rain showers": ":rain_cloud:",
        "moderate rain showers": ":rain_cloud:",
        "violent rain showers": ":rain_cloud:",
        "slight snow showers": ":snowflake:",
        "heavy snow showers": ":snowflake:",
        "thunderstorm": ":lightning_cloud:",
        "thunderstorm with slight hail": ":lightning_cloud:",
        "thunderstorm with heavy hail": ":lightning_cloud:"
    }
    temp_emojis = {
        "hot": ":hot_face:",
        "warm": ":sunglasses:",
        "cool": ":relieved:",
        "cold": ":cold_face:"
    }

    emoji = weather_emojis.get(description, ":question:")
    
    if temperature > 30:
        temp_emoji = temp_emojis["hot"]
    elif temperature > 20:
        temp_emoji = temp_emojis["warm"]
    elif temperature > 10:
        temp_emoji = temp_emojis["cool"]
    else:
        temp_emoji = temp_emojis["cold"]

    return emoji + " " + temp_emoji
