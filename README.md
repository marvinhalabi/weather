# Weather + News App :sun_with_face:

A Streamlit application that provides current weather information and the latest news for any city worldwide. The app retrieves data from Open-Meteo and news articles using the NewsData.io API.

## Features

- :thermometer: **Current Weather**: Displays the current temperature, wind speed, and weather conditions.
- :sunrise: **Sunrise and Sunset Times**: Shows the local sunrise and sunset times for the selected city.
- :bar_chart: **Hourly Forecast**: Plots an hourly temperature forecast.
- :newspaper: **City News**: Fetches and displays recent news articles from the selected city.
- :earth_africa: **Autocomplete City Search**: Uses a search box with autocomplete to help find cities easily.

## Tech Stack

- **Streamlit**: For the front-end web app framework.
- **Open-Meteo API**: For weather data.
- **NewsData.io API**: For fetching news articles.
- **Pandas**: For handling and processing city data.
- **Matplotlib**: For plotting the hourly temperature forecast.

## Installation

To run the app locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/marvinhalabi/weather.git
   ```

2. Navigate to the project directory:

   ```bash
   cd weather
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add your API keys:
   
   - Create a `.env` file in the root of the project.
   - Add your `NEWS_API_KEY` like this:

     ```
     NEWS_API_KEY=your_news_api_key_here
     ```

5. Run the app:

   ```bash
   streamlit run app.py
   ```

## Usage

1. Start the application and enter the name of a city in the search box.
2. The app will fetch the weather data, including the current temperature, wind speed, and local sunrise/sunset times.
3. You'll also see a plot of the hourly temperature forecast for the next 24 hours.
4. Below the weather data, the app will display the latest news articles for the selected city.

## File Structure

```
.
├── app.py                # Main Streamlit app file
├── requirements.txt      # Python dependencies
├── Procfile              # For Heroku deployment (optional)
├── .env                  # Environment variables for API keys
├── worldcities.csv       # CSV file containing city data
└── weather_utils.py      # Utility functions for weather description and emojis
```

## Environment Variables

Make sure to configure the following environment variables:

- **NEWS_API_KEY**: Your API key from NewsData.io.

## Screenshots

![Weather App Screenshot]("weather-news-screen.gif")

## License

This project is licensed under the MIT License.

---

### Notes:
- Replace `"path-to-screenshot"` with the actual path if you want to add screenshots.
- Ensure your `.env` file is included in `.gitignore` to prevent exposing sensitive API keys.

Feel free to adjust the content based on your specific needs! Let me know if you want any changes.
