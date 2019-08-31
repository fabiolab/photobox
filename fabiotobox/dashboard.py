from fabiotobox.weather import Weather
from fabiotobox.weather_service import WeatherService
from PIL import Image, ImageDraw, ImageFont
import pendulum

DASHBOARD_BACKGROUND = "static/templates/dashboard_template.png"
DASHBOARD_IMG = "static/dashboard.png"


TRANSLATE_DAY = {
    "monday": "lundi",
    "tuesday": "mardi",
    "wednesday": "mercredi",
    "thursday": "jeudi",
    "friday": "vendredi",
    "saturday": "samedi",
    "sunday": "dimanche",
}

TRANSLATE_MONTH = {
    "january": "janvier",
    "february": "février",
    "march": "mars",
    "april": "avril",
    "may": "mai",
    "june": "juin",
    "july": "juillet",
    "august": "août",
    "september": "septembre",
    "october": "octobre",
    "november": "novembre",
    "december": "décembre",
}


class Dashboard:
    def __init__(self, weather_service: WeatherService):
        self.image = Dashboard.init_dashboard()
        self.weather_service = weather_service

    @staticmethod
    def init_dashboard():
        img = Image.open(DASHBOARD_BACKGROUND)
        return img

    def add_image(self, image: str, pos_x: int, pos_y: int):
        img = Image.open(image)
        self.image.paste(img, (pos_x, pos_y), img)

    def add_text(self, text: str, pos_x: int, pos_y: int, size: int):
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("static/fonts/CaviarDreams.ttf", size)
        draw.text((pos_x, pos_y), text, (255, 255, 255), font=font)

    def add_date(self, size: int):
        dt = pendulum.now("Europe/Paris")
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("static/fonts/CaviarDreams.ttf", size)

        w, h = self.image.size

        dayofweek = TRANSLATE_DAY.get(dt.format("dddd").lower())
        month = TRANSLATE_MONTH.get(dt.format("MMMM").lower())
        text = dayofweek + dt.format(" DD ") + month
        date_w, date_h = draw.textsize(text, font=font)

        draw.text(
            (int((w - date_w) / 2), int((h - date_h) / 2)), text, (255, 255, 255), font=font
        )

        text = dt.format("HH:mm")
        hour_w, hour_h = draw.textsize(text, font=font)

        draw.text(
            (int((w - hour_w) / 2), int((h - hour_h) / 2) + date_h), text, (255, 255, 255), font=font
        )

    def add_hour(self, pos_x: int, pos_y: int, size: int):
        dt = pendulum.now("Europe/Paris")
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("static/fonts/CaviarDreams.ttf", size)
        draw.text((pos_x, pos_y), dt.format("HH:mm"), (255, 255, 255), font=font)

    def add_weather(
        self,
        weather: Weather,
        pos_x: int,
        pos_y: int,
        img_percent_size: int = 50,
        font_size: int = 50,
    ):
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("static/fonts/CaviarDreams.ttf", font_size)

        dt = TRANSLATE_DAY.get(weather.datetime.format("dddd").lower())
        dt_w, dt_h = draw.textsize(dt, font=font)

        temperature = str(int(weather.temperature))
        temp_w, temp_h = draw.textsize(temperature, font=font)

        img = Image.open("static/icons/{}.png".format(weather.icon))
        img = self.resize(img, img_percent_size)
        img_w, img_h = img.size

        # self.image.paste(img, (pos_x, pos_y), img)

        self.add_text(dt, pos_x + (img_w - dt_w) / 2, pos_y - dt_h, font_size)
        self.image.paste(img, (pos_x, pos_y), img)
        self.add_text(
            "{}°".format(temperature),
            pos_x + (img_w - temp_w) / 2,
            pos_y + img_h,
            font_size,
        )

    def validate(self):
        self.image.save(DASHBOARD_IMG)

    @staticmethod
    def resize(img: Image, percent: int):
        wsize = int((float(img.size[0]) * (percent / 100)))
        hsize = int((float(img.size[1]) * (percent / 100)))
        return img.resize((wsize, hsize), Image.ANTIALIAS)

    def update_dashboard(self):
        weather = self.weather_service.get_current_weather()
        forecast = self.weather_service.get_forecast_weather_by_day()

        self.add_weather(weather, 50, 50, 100, 50)
        for i, w in enumerate(forecast):
            self.add_weather(w, 200 + 220 * (i + 1), 50)

        self.add_date(size=100)
