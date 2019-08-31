from fabiotobox.dashboard import Dashboard
from fabiotobox.weather_service import WeatherService
from loguru import logger

WEATHER_APP_ID = "5c4fda780eaf777a20f64b3352da96b2"
WEATHER_BASE_URL = "http://api.openweathermap.org/"
WEATHER_ENDPOINT = "/data/2.5/weather"
WEATHER_FORECAST_ENDPOINT = "/data/2.5/forecast"
WEATHER_CITY = "rennes,fr"

if __name__ == "__main__":
    logger.info("Run ...")

    my_weather_service = WeatherService(
        base_url=WEATHER_BASE_URL,
        end_point_weather=WEATHER_ENDPOINT,
        end_point_forecast=WEATHER_FORECAST_ENDPOINT,
        city=WEATHER_CITY,
        appid=WEATHER_APP_ID,
    )
    weather = my_weather_service.get_current_weather()
    forecast = my_weather_service.get_forecast_weather_by_day()

    dash = Dashboard()
    dash.add_weather(weather, 50, 50, 100, 50)
    for i, w in enumerate(forecast):
        dash.add_weather(w, 200 + 220 * (i+1), 50)

    dash.add_date(size=100)
    dash.image.show()
    logger.info("Init done !")
