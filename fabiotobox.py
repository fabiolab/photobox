from loguru import logger
from fabiotobox.fabiotobox import Fabiotobox
from fabiotobox.camera import Camera
from fabiotobox.photohandler import PhotoHandler
from fabiotobox.tumblr import Tumblr
import click


@click.command()
@click.option(
    "--event_title", prompt="Event Title", help="Title for tumblr posts description"
)
def run():
    logger.debug("Running fabiotobox ...")
    camera = Camera(storage_dir="photos/", rotate=180, fullscreen=False)
    photo_handler = PhotoHandler(storage_dir="photos/")
    tumblr = Tumblr(
        "N89rMJVwVBR0IrjZ8tRK3WJkGhIDQQT8Cr0zJ33sVVxSToOpno",
        "TdKV5P0mCmGII2WFYUuQFe0xAwsvi1wrW7OhGZ9ydOKDSoOQpS",
        "387VYuXTw8X3VigZiT1YAuGDIIbFcM43Ff4fMUlbkyKT2FT0dy",
        "dErS8RPiyLUcWMkxhMsNWM2kLfA9KskYGo0gbEbl5Q1VykstFk",
        blog_name="fabiotobox",
    )
    fabiotobox = Fabiotobox(
        camera=camera, photo_handler=photo_handler, tumblr=tumblr, shoot_button_port=18
    )
    fabiotobox.run()


if __name__ == "__main__":
    run()
