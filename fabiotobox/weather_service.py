from fabiotobox.weather import Weather, WeatherCondition
import pendulum
from loguru import logger
import requests
from typing import List
from urllib.parse import urljoin
from expiringdict import ExpiringDict


class WeatherService:
    def __init__(
        self,
        base_url: str,
        end_point_weather: str,
        end_point_forecast: str,
        city: str,
        appid: str,
    ):
        self._yesterday_forecast = None

        self.weather_url = urljoin(base_url, end_point_weather)
        self.forecast_url = urljoin(base_url, end_point_forecast)
        self.city = city
        self.appid = appid
        self.cache = ExpiringDict(max_len=100, max_age_seconds=3600)

    def get_current_weather(self) -> Weather:
        if self.cache.get("weather", None):
            return self.cache.get("weather")
            
        logger.info("Getting current weather")
        parameter = {"q": self.city, "APPID": self.appid, "units": "metric"}
        try:
            logger.info("Calling {} for getting weather".format(self.weather_url))
            response = requests.get(self.weather_url, params=parameter)
            if response.status_code >= 400:
                e = Exception(
                    "HTTP Error calling {} => {} : {}".format(
                        self.weather_url, response.status_code, response.text
                    )
                )
                logger.error(e)
                raise e
            response_json = response.json()
            current_weather = self.parse_single_weather(response_json)
            self.cache["weather"] = current_weather
            return current_weather
        except Exception as e:
            logger.error(e)
            raise e


    def get_forecast_weather(self) -> List[Weather]:
        if self.cache.get("forecast_weather", None):
            return self.cache.get("forecast_weather")

        logger.info("Getting forecast weather")
        parameter = {"q": self.city, "APPID": self.appid, "units": "metric"}
        try:
            response = requests.get(self.forecast_url, params=parameter)
            if response.status_code >= 400:
                e = Exception(
                    "HTTP Error calling {} => {} : {}".format(
                        self.forecast_url, response.status_code, response.text
                    )
                )
                logger.error(e)
                raise e
            response_json = response.json()
            forecast_weather = [
                self.parse_single_weather(forecast)
                for forecast in response_json.get("list", [])
            ]
            self.cache["forecast_weather"] = forecast_weather
            return forecast_weather
        except Exception as e:
            logger.error(e)
            raise e

    # Get one forecast by day from the current date
    def get_forecast_weather_by_day(self) -> List[Weather]:
        logger.info("Getting forecast weather by day")
        forecast_by_day = list()

        forecast = self.get_forecast_weather()
        dt = pendulum.now("Europe/Paris")

        # For each day, get only the forecast in the range 12:00 to 14:00 (forecast are given by range of 3 hours)
        for weather in forecast:
            if weather.datetime.hour in [12, 13, 14]:
                forecast_by_day.append(weather)

        return forecast_by_day

    @staticmethod
    def parse_single_weather(weather_raw: dict) -> Weather:
        weather = Weather()

        weather.temperature = weather_raw.get("main", {}).get("temp")
        weather.humidity = weather_raw.get("main", {}).get("humidity")
        weather.wind_speed = weather_raw.get("wind", {}).get("speed")
        weather.datetime = pendulum.from_timestamp(weather_raw.get("dt"))
        weather.icon = weather_raw.get("weather", [])[0].get("icon")

        # Weather conditions are described here : https://openweathermap.org/weather-conditions
        main_description = weather_raw.get("weather", [])
        for condition in main_description:
            weather.conditions.append(
                WeatherService._get_condition_from_id(condition["id"])
            )

        return weather

    @staticmethod
    def _get_condition_from_id(id_condition):
        if id_condition // 100 == 8:
            logger.debug("{} : Clear or Cloudy".format(id_condition))
            return WeatherCondition.CLEAR
        if id_condition // 100 == 7:
            logger.debug("{} : Foggy".format(id_condition))
            return WeatherCondition.FOG
        if id_condition // 100 == 6:
            logger.debug("{} : Snow".format(id_condition))
            return WeatherCondition.SNOW
        if id_condition // 100 == 5:
            logger.debug("{} : Rainy".format(id_condition))
            return WeatherCondition.RAIN
        if id_condition // 100 == 3:
            logger.debug("{} : Drizzle (bruine in french)".format(id_condition))
            return WeatherCondition.DRIZZLE
        if id_condition // 100 == 2:
            logger.debug("{} : Thunderstorm".format(id_condition))
            return WeatherCondition.THUNDERSTORM
