from loguru import logger
from fabiotobox.fabiotobox import Fabiotobox
from fabiotobox.camera import Camera
from fabiotobox.photohandler import PhotoHandler
from fabiotobox.diaporama import Diaporama
from fabiotobox.tumblr import Tumblr

PHOTO_DIR = "/media/pi/2078B0CD25633F53/Backup/Photos/2016"


def run():
    logger.debug("Running fabiotobox ...")
    camera = Camera(storage_dir="photos/", rotate=0, fullscreen=True)
    diapo = Diaporama(PHOTO_DIR)
    photo_handler = PhotoHandler(storage_dir="photos/")
    tumblr = Tumblr()
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
