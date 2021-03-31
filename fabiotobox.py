import os

from loguru import logger
from fabiotobox.fabiotobox import Fabiotobox
from fabiotobox.camera import Camera
from fabiotobox.photohandler import PhotoHandler
from fabiotobox.diaporama import Diaporama
from fabiotobox.tumblr import Tumblr

PHOTO_DIR = os.environ.get("PHOTO_DIR")


def run():
    logger.debug("Running fabiotobox ...")
    camera = Camera(storage_dir="photos/", rotate=0, fullscreen=True)
    diapo = Diaporama(photo_folder=PHOTO_DIR)
    photo_handler = PhotoHandler(storage_dir="photos/")
    tumblr = Tumblr(
        os.environ.get("CONSUMER_KEY"),
        os.environ.get("CONSUMER_SECRET"),
        os.environ.get("OAUTH_TOKEN"),
        os.environ.get("OAUTH_SECRET"),
        os.environ.get("BLOG_NAME")
    )
    fabiotobox = Fabiotobox(
        camera=camera,
        diaporama=diapo,
        photo_handler=photo_handler,
        tumblr=tumblr,
        shoot_button_port=18,
    )
    fabiotobox.run()


if __name__ == "__main__":
    run()
