from loguru import logger
from fabiotobox.fabiotobox import Fabiotobox
from fabiotobox.camera import Camera
from fabiotobox.photohandler import PhotoHandler
from fabiotobox.tumblr import Tumblr
import click


# @click.command()
# @click.option(
#    "--event_title", prompt="Event Title", help="Title for tumblr posts description"
#)
def run():
    logger.debug("Running fabiotobox ...")
    camera = Camera(storage_dir="photos/", rotate=0, fullscreen=True)
    photo_handler = PhotoHandler(storage_dir="photos/")
    tumblr = Tumblr(
    )
    fabiotobox = Fabiotobox(
        camera=camera, photo_handler=photo_handler, tumblr=tumblr, shoot_button_port=18
    )
    fabiotobox.run()


if __name__ == "__main__":
    run()
