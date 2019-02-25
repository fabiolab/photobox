from loguru import logger
from gpiozero import Button
from fabiotobox.camera import Camera
from fabiotobox.photohandler import PhotoHandler

if __name__ == "__main__":
    logger.debug("Running fabiotobox ...")
    camera = Camera(storage_dir="./", rotate=180)
    photo_handler = PhotoHandler(storage_dir="./")

    logger.debug("Initializing input button ...")
    button = Button(18)
    # button.when_pressed = camera.shoot
    button.when_held = camera.end

    camera.start_preview()

    while True:
        if button.when_pressed:
            logger.debug("Button pressed")
            pictures = camera.shoot()
            photo = photo_handler.combine(pictures)
            camera.display_image(photo)

