from loguru import logger
from fabiotobox.fabiotobox import Fabiotobox
from fabiotobox.camera import Camera
from fabiotobox.photohandler import PhotoHandler
from fabiotobox.diaporama import Diaporama
from fabiotobox.tumblr import Tumblr
from fabiotobox.weather_service import WeatherService
from fabiotobox.dashboard import Dashboard

PHOTO_DIR = "/media/pi/2078B0CD25633F53/Backup/Photos"
WEATHER_APP_ID = "5c4fda780eaf777a20f64b3352da96b2"
WEATHER_BASE_URL = "http://api.openweathermap.org/"
WEATHER_ENDPOINT = "/data/2.5/weather"
WEATHER_FORECAST_ENDPOINT = "/data/2.5/forecast"
WEATHER_CITY = "rennes,fr"

def run():
    logger.debug("Running fabiotobox ...")
    my_weather_service = WeatherService(
        base_url=WEATHER_BASE_URL,
        end_point_weather=WEATHER_ENDPOINT,
        end_point_forecast=WEATHER_FORECAST_ENDPOINT,
        city=WEATHER_CITY,
        appid=WEATHER_APP_ID,
    )
    weather = my_weather_service.get_current_weather()
    forecast = my_weather_service.get_forecast_weather_by_day()

    camera = Camera(storage_dir="photos/", rotate=0, fullscreen=True)
    diapo = Diaporama(photo_folder=PHOTO_DIR)
    dashboard = Dashboard(my_weather_service)
    photo_handler = PhotoHandler(storage_dir="photos/")
    tumblr = Tumblr(
        "N89rMJVwVBR0IrjZ8tRK3WJkGhIDQQT8Cr0zJ33sVVxSToOpno",
        "TdKV5P0mCmGII2WFYUuQFe0xAwsvi1wrW7OhGZ9ydOKDSoOQpS",
        "387VYuXTw8X3VigZiT1YAuGDIIbFcM43Ff4fMUlbkyKT2FT0dy",
        "dErS8RPiyLUcWMkxhMsNWM2kLfA9KskYGo0gbEbl5Q1VykstFk",
        # blog_name="manonetguillaume",
        blog_name="fabiotobox",
    )
    fabiotobox = Fabiotobox(
        camera=camera,
        diaporama=diapo,
        dashboard=dashboard,
        photo_handler=photo_handler,
        tumblr=tumblr,
        shoot_button_port=18,
    )
    fabiotobox.run()


if __name__ == "__main__":
    run()
