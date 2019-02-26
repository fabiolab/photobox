from loguru import logger
from gpiozero import Button
from fabiotobox.camera import Camera
from fabiotobox.photohandler import PhotoHandler
from fabiotobox.tumblr import Tumblr
from enum import IntEnum


class PhotoFormat(IntEnum):
    PHOTOBOX = 0
    POLAROID = 1


class Fabiotobox:
    def __init__(
        self,
        camera: Camera,
        photo_handler: PhotoHandler,
        tumblr: Tumblr,
        shoot_button_port: int,
        effect_button_port: int = None,
        format_button_port: int = None,
        event_title: str = "Test",
    ):
        self.shoot_button = Button(shoot_button_port)
        self.effect_button = Button(effect_button_port)
        self.format_button = Button(format_button_port)
        self.camera = camera
        self.photo_handler = photo_handler
        self.tumblr = tumblr
        self.photo_format = PhotoFormat.PHOTOBOX
        self.event_title = event_title

    def run(self):
        self.shoot_button.when_held = self.camera.end
        self.camera.start_preview()

        while True:
            if self.shoot_button.is_pressed:
                logger.debug("Button pressed")
                photo = self.handle_button_pressed()
                self.camera.display_image(photo)

                logger.info("Sending {} to tumblr".format(photo))
                self.tumblr.post_photo(photo, self.event_title, [])

    def handle_button_pressed(self) -> str:
        if self.photo_format == PhotoFormat.POLAROID:
            pictures = self.camera.shoot(1)
            photo = self.photo_handler.polaroid(pictures[0])
        else:
            pictures = self.camera.shoot(3)
            photo = self.photo_handler.combine(pictures)

        return photo
