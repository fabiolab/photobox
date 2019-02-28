from time import sleep
from datetime import datetime
import picamera
from os import path
from PIL import Image
from loguru import logger


class Camera:
    def __init__(
        self,
        storage_dir: str,
        rotate: int = 0,
        text_size: int = 160,
        fullscreen: bool = True,
    ):
        self.camera = picamera.PiCamera()
        self.storage_dir = storage_dir
        self.camera.rotation = rotate
        self.camera.annotate_text_size = text_size
        self.fullscreen = fullscreen

    def start_preview(self):
        logger.debug("Running preview ...")

        self.camera.start_preview(
            resolution=(self.camera.resolution[0] // 2, self.camera.resolution[1] // 2),
            window=(300, 100, 640, 480),
            fullscreen=self.fullscreen,
        )

    def shoot(self, num_pictures: int = 3) -> list:
        logger.debug("Shooting {} photos".format(num_pictures))

        self.countdown()

        pictures = self.generate_photo_names(num_pictures)
        for pic in pictures:
            self.flash()
            logger.debug("Shooting {}".format(pic))
            self.camera.capture(pic)
            sleep(1)

        return pictures

    def countdown(self, start: int = 3):
        for i in range(start, 0, -1):
            logger.debug("Countdown {}".format(i))
            self.camera.annotate_text = "{}".format(i)
            sleep(1)
        self.camera.annotate_text = ""

    def flash(self):
        logger.debug("Flash !!")
        self.camera.brightness = 80
        sleep(0.3)
        self.camera.brightness = 50

    def generate_photo_names(self, num_pictures: int = 3) -> list:
        now = datetime.now()
        picture_name = now.strftime("%Y%m%d_%H%M%S")
        logger.debug("Base name for current pictures : {}".format(picture_name))

        return [
            path.join(self.storage_dir, "{}_{}.jpeg".format(picture_name, i))
            for i in range(num_pictures)
        ]

    def end(self):
        logger.info("End of the party !")
        self.camera.close()

    def display_image(self, image: str, delay: int = 3):
        logger.debug("Displaying {} for {} seconds".format(image, delay))
        img = Image.open(image)
        thumbnail = img.thumbnail(self.camera.resolution, Image.ANTIALIAS)

        # The width must be a multiple of 32
        # The height must be a multiple of 16
        # cf add_overlay documentation
        background_image = Image.new(
            "RGB",
            (
                ((self.camera.resolution[0] + 31) // 32) * 32,
                ((self.camera.resolution[1] + 15) // 16) * 16,
            ),
        )

        # Paste the original image a the center of the image
        center_x = self.camera.resolution[0] // 2 - img.size[0] // 2
        center_y = self.camera.resolution[1] // 2 - img.size[1] // 2
        background_image.paste(img, (center_x, center_y))

        # Add the overlay with the new image as the source
        o = self.camera.add_overlay(
            background_image.tobytes(), size=self.camera.resolution
        )

        # To make the new overlay semi-transparent use :
        # o.alpha = 128

        # By default, the overlay is in layer 0, beneath the preview (which defaults to layer 2)
        o.layer = 3

        sleep(delay)
        self.camera.remove_overlay(o)
