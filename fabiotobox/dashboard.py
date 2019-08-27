from fabiotobox.weather import Weather
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


class Dashboard:
    def __init__(self):
        self.image = Dashboard.init_dashboard()

    @staticmethod
    def init_dashboard():
        img = Image.open(DASHBOARD_BACKGROUND)
        return img

    def add_image(self, image: str, pos_x: int, pos_y: int):
        img = Image.open(image)
        self.image.paste(img, (pos_x, pos_y), img)

    def add_text(self, text: str, pos_x: int, pos_y: int, size: int):
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("static/fonts/theboldfont.ttf", size)
        draw.text((pos_x, pos_y), text, (255, 255, 255), font=font)

    def add_date(self, pos_x: int, pos_y: int, size: int):
        dt = pendulum.now("Europe/Paris")
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("static/fonts/theboldfont.ttf", size)
        draw.text((pos_x, pos_y), dt.format("DD MM YYYY"), (255, 255, 255), font=font)

    def add_hour(self, pos_x: int, pos_y: int, size: int):
        dt = pendulum.now("Europe/Paris")
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("static/fonts/theboldfont.ttf", size)
        draw.text((pos_x, pos_y), dt.format("HH:mm"), (255, 255, 255), font=font)

    def add_weather(self, weather: Weather, pos_x: int, pos_y: int, size: int):
        self.add_text(
            TRANSLATE_DAY.get(weather.datetime.format("dddd").lower()),
            pos_x,
            pos_y - 50,
            size,
        )
        self.add_image("static/icons/{}.png".format(weather.icon), pos_x, pos_y)
        self.add_text("{}°".format(int(weather.temperature)), pos_x + 50, pos_y + 200, size)

    def validate(self):
        self.image.save(DASHBOARD_IMG)
