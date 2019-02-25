from gpiozero import Button
from time import sleep
from datetime import datetime
import picamera
from PIL import Image, ImageDraw
import os
import sys

'''
    Push button : 
        - Fait clignoter une led indiquant le compte à rebours + compte à rebours sur l'écran
        - Allume une led pour chaque prise de vue (3 ou 4 consécutives) + flash l'écran pour chaque prise de vue (1 seconde entre chacune des 4 prises)
        - Les photos sont enregistrées puis assemblées verticalement
        - La photo finale est postée sur le net
    Bouton mode : B&W -> B&W + Vintage -> Vintage -> Normal -> B&W -> ...
    Bouton last : Affiche la dernière photo

    Bush button long : quitter l'appli
'''

def end():
    camera.close()
    sys.exit(0)

def flash():
    # Simulate the flash
    camera.brightness = 80
    sleep(0.3)
    camera.brightness = 50
    
def shoot(num_pic:int=3) -> list:
    camera.annotate_text = "3"
    sleep(1)
    camera.annotate_text = "2"
    sleep(1)
    camera.annotate_text = "1"
    sleep(1)
    camera.annotate_text = ""

    now = datetime.now()
    picture_name = now.strftime('%Y%m%d_%H%M%S')
    pictures = ['{}_{}.jpeg'.format(picture_name, i) for i in range(num_pic)]

    # capture_sequence does the job but doesn't simulate a flash
    # camera.capture_sequence(pictures)

    for pic in pictures:
        flash() 
        camera.capture(pic)
        sleep(1)

    shot = combine(picture_name, pictures)
    print("sending photo to tumblr")
    client.create_photo("fabiotobox", state="queue", tags=["testing", "ok"],
                    tweet="Woah this is an incredible sweet post [URL]",
                    data=shot)



def _add_corners(im, rad=100):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, "white")
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def combine(base_name:str, files:list) -> str:
    output_name = '{}.jpeg'.format(base_name)

    result = Image.new("RGB", (420, 790))

    for index, file in enumerate(files):
        path = os.path.expanduser(file)
        img = Image.open(path)
        img = _add_corners(img)
        img.thumbnail((400, 400), Image.ANTIALIAS)
        w, h = img.size
        x = 10
        y = 10 + index * 260
        print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
        result.paste(img, (x, y, x + w, y + h))

    result.save(os.path.expanduser(output_name))
    o = display(output_name)
    sleep(3)
    camera.remove_overlay(o)
    return output_name

def display(image):
    img = Image.open(image)

    # Create the support image that will take all the screen
    background_image = Image.new("RGB", camera.resolution)
    
    # The width must be a multiple of 32
    # The height must be a multiple of 16
    # cf add_overlay documentation
    background_image = Image.new('RGB', (
                        ((camera.resolution[0] + 31) // 32) * 32,
                        ((camera.resolution[1] + 15) // 16) * 16,
                        ))
    
    # Paste the original image into the padded one
    # Center the image
    center_x = camera.resolution[0]//2 - img.size[0]//2
    center_y = camera.resolution[1]//2 - img.size[1]//2
    
    background_image.paste(img, (center_x, center_y))

    # Add the overlay with the padded image as the source,
    # but the original image's dimensions
    o = camera.add_overlay(background_image.tobytes(),
                           size=camera.resolution)
    # By default, the overlay is in layer 0, beneath the
    # preview (which defaults to layer 2). Here we make
    # the new overlay semi-transparent, then move it above
    # the preview
    # o.alpha = 128
    o.layer = 3
    return o

import pytumblr

client = pytumblr.TumblrRestClient(
  'N89rMJVwVBR0IrjZ8tRK3WJkGhIDQQT8Cr0zJ33sVVxSToOpno',
  'TdKV5P0mCmGII2WFYUuQFe0xAwsvi1wrW7OhGZ9ydOKDSoOQpS',
  '387VYuXTw8X3VigZiT1YAuGDIIbFcM43Ff4fMUlbkyKT2FT0dy',
  'dErS8RPiyLUcWMkxhMsNWM2kLfA9KskYGo0gbEbl5Q1VykstFk'
)

client.info()


camera = picamera.PiCamera()
camera.rotation = 180
camera.flash_mode = "auto"
camera.annotate_text_size = 160
# camera.color_effects = (128,128) # turn camera to black and white
camera.start_preview(resolution=(camera.resolution[0]//2, camera.resolution[1]//2),
                     fullscreen=False,
                     window = (300, 100, 640, 480))

button = Button(18)
button.when_pressed = shoot
button.when_held = end

