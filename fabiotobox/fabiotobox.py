from loguru import logger
from gpiozero import Button
from fabiotobox.camera import Camera
from fabiotobox.photohandler import PhotoHandler
from fabiotobox.tumblr import Tumblr
from enum import IntEnum
import pendulum
import glob
import random
import time

SCREENSAVER_DELAY = 1
PHOTO_DIR = "photos"


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
        tumblr: Tumblr,
        shoot_button_port: int,
        effect_button_port: int = None,
        format_button_port: int = None,
        event_title: str = "Test"
    ):
        self.shoot_button = Button(shoot_button_port)
        if effect_button_port:
            self.effect_button = Button(effect_button_port)
        if format_button_port:
            self.format_button = Button(format_button_port)
        self.camera = camera
        self.photo_handler = photo_handler
        self.tumblr = tumblr
        self.photo_format = PhotoFormat.POLAROID
        self.event_title = event_title
        self.mode = Mode.PHOTOBOX
        self.diaporama_countdown = pendulum.now('Europe/Paris')
        self.photos = list()

    def run(self):
        self.load_photos(PHOTO_DIR)
        self.shoot_button.when_held = self.camera.end
        self.camera.start_preview()
        self.reset_diaporama_countdown()

        while True:
            if self.is_diaporama_countdown_reached():
                self.mode = Mode.DIAPORAMA
            else:
                self.mode = Mode.PHOTOBOX

            if self.mode is Mode.PHOTOBOX:
                self.run_photobox()
            else:
                self.run_diaporama()

    def run_photobox(self):
        if self.shoot_button.is_pressed:
            logger.debug("Button pressed for a photo")
            photo = self.handle_button_pressed()
            self.camera.display_image(photo)
            time.sleep(3)
            self.camera.undisplay_image()

            logger.info("Sending {} to tumblr".format(photo))
            self.tumblr.post_photo(photo, self.event_title, [])

    def run_diaporama(self):
        if self.shoot_button.is_pressed:
            logger.debug("Button pressed for exiting diaporama")
            self.mode = Mode.PHOTOBOX
            self.camera.undisplay_image()
            self.reset_diaporama_countdown()
        else:
            if self.is_diaporama_countdown_reached():
                # self.camera.undisplay_image()
                self.camera.display_image(random.choice(self.photos))
                self.reset_diaporama_countdown()

    def handle_button_pressed(self) -> str:
        if self.photo_format == PhotoFormat.POLAROID:
            pictures = self.camera.shoot(1)
            photo = self.photo_handler.polaroid(pictures[0])
        else:
            pictures = self.camera.shoot(3)
            photo = self.photo_handler.combine(pictures)

        return photo

    def reset_diaporama_countdown(self):
        self.diaporama_countdown = pendulum.now('Europe/Paris').add(minutes=SCREENSAVER_DELAY)

    def is_diaporama_countdown_reached(self) -> bool:
        return self.diaporama_countdown < pendulum.now('Europe/Paris')

    def load_photos(self, dir_path: str):
        logger.debug("Loading photos from {}".format(dir_path))
        self.photos = [
            filename for filename in glob.glob("{}/**/*.jpeg".format(dir_path), recursive=True)
        ]
        logger.debug("{} photos loaded from {}".format(len(self.photos), dir_path))
