from loguru import logger
from gpiozero import Button
from fabiotobox.camera import Camera
from fabiotobox.photohandler import PhotoHandler
from fabiotobox.tumblr import Tumblr


if __name__ == "__main__":
    logger.debug("Running fabiotobox ...")
    camera = Camera(storage_dir="./", rotate=180, fullscreen=False)
    photo_handler = PhotoHandler(storage_dir="./")

    logger.debug("Initializing input button ...")
    button = Button(18)
    # button.when_pressed = camera.shoot
    button.when_held = camera.end

    camera.start_preview()

    tumblr = Tumblr('N89rMJVwVBR0IrjZ8tRK3WJkGhIDQQT8Cr0zJ33sVVxSToOpno',
                    'TdKV5P0mCmGII2WFYUuQFe0xAwsvi1wrW7OhGZ9ydOKDSoOQpS',
                    '387VYuXTw8X3VigZiT1YAuGDIIbFcM43Ff4fMUlbkyKT2FT0dy',
                    'dErS8RPiyLUcWMkxhMsNWM2kLfA9KskYGo0gbEbl5Q1VykstFk',
                    blog_name = 'fabiotobox')
    
    mode_polaroid = False

    while True:
        if button.is_pressed:
            logger.debug("Button pressed")
            if mode_polaroid:
                pictures = camera.shoot(1)
                photo = photo_handler.polaroid(pictures[0])
            else:
                pictures = camera.shoot(3)
                photo = photo_handler.combine(pictures)
            camera.display_image(photo)

            logger.info("Sending {} to tumblr".format(photo))
            tumblr.post_photo(photo, "test", ["ok"])
 