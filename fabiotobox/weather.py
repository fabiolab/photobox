from enum import Enum
import pendulum


class WeatherCondition(Enum):
    CLEAR = 1
    FOG = 2
    SNOW = 3
    RAIN = 4
    DRIZZLE = 5
    THUNDERSTORM = 6


class Weather:
    def __init__(self):
        self.temperature = 0.0
        self.conditions = []
        self.wind_speed = 0.0
        self.humidity = 0
        self.datetime = pendulum.now("Europe/Paris")
        self.icon = "01d"

    def __str__(self) -> str:
        return "{};{};{};{}".format(
            self.temperature, self.conditions, self.wind_speed, self.humidity
        )
