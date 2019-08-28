from loguru import logger
from gpiozero import Button
from fabiotobox.camera import Camera
from fabiotobox.diaporama import Diaporama
from fabiotobox.photohandler import PhotoHandler
from fabiotobox.tumblr import Tumblr
from enum import IntEnum
import pendulum
import time

SCREENSAVER_DELAY = 1


class PhotoFormat(IntEnum):
    PHOTOBOX = 0
    POLAROID = 1


class Mode(IntEnum):
    PHOTOBOX = 0
    DIAPORAMA = 1


class Fabiotobox:
    def __init__(
        self,
        camera: Camera,
        photo_handler: PhotoHandler,
        diaporama: Diaporama,
        tumblr: Tumblr,
        shoot_button_port: int,
        effect_button_port: int = None,
        format_button_port: int = None,
        event_title: str = "Test",
    ):
        self.shoot_button = Button(shoot_button_port)
        if effect_button_port:
            self.effect_button = Button(effect_button_port)
        if format_button_port:
            self.format_button = Button(format_button_port)
        self.camera = camera
        self.photo_handler = photo_handler
        self.diaporama = diaporama
        self.tumblr = tumblr
        self.photo_format = PhotoFormat.POLAROID
        self.event_title = event_title
        self.mode = Mode.PHOTOBOX
        self.diaporama_countdown = pendulum.now("Europe/Paris")

    def run(self):
        self.shoot_button.when_held = self.camera.end
        self.camera.start_preview()
        self.reset_diaporama_countdown()

        while True:
            if self.is_diaporama_countdown_reached():
                self.mode = Mode.DIAPORAMA

            if self.mode is Mode.PHOTOBOX:
                self.run_photobox()
            else:
                self.run_diaporama()

    def run_photobox(self):
        if self.shoot_button.is_pressed:
            logger.debug("Button pressed for a photo")
            photo = self.shoot_photo()
            self.camera.display_image(photo)
            time.sleep(3)
            self.camera.undisplay_image()

            logger.info("Sending {} to tumblr".format(photo))
            self.tumblr.post_photo(photo, self.event_title, [])
            self.reset_diaporama_countdown()

    def run_diaporama(self):
        if self.shoot_button.is_pressed:
            logger.debug("Button pressed for exiting diaporama")
            self.mode = Mode.PHOTOBOX
            self.camera.undisplay_image()
            self.reset_diaporama_countdown()
            time.sleep(1)  # prevent event to be catched by photobox too
        else:
            if self.is_diaporama_countdown_reached():
                logger.info("dirs : {}".format(len(self.diaporama.dirs)))
                self.camera.display_image(self.diaporama.pick_photo())
                self.reset_diaporama_countdown()

    def shoot_photo(self) -> str:
        if self.photo_format == PhotoFormat.POLAROID:
            pictures = self.camera.shoot(1)
            photo = self.photo_handler.make_polaroid(pictures[0])
        else:
            pictures = self.camera.shoot(3)
            photo = self.photo_handler.make_photostrip(pictures)

        return photo

    def reset_diaporama_countdown(self):
        self.diaporama_countdown = pendulum.now("Europe/Paris").add(
            minutes=SCREENSAVER_DELAY
        )

    def is_diaporama_countdown_reached(self) -> bool:
        return self.diaporama_countdown < pendulum.now("Europe/Paris")
