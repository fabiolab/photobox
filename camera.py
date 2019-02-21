from gpiozero import Button
from time import sleep
from datetime import datetime
import picamera
import pygame
from PIL import Image
import os

'''
    Push button : 
        - Fait clignoter une led indiquant le compte à rebours + compte à rebours sur l'écran
        - Allume une led pour chaque prise de vue (3 ou 4 consécutives) + flash l'écran pour chaque prise de vue (1 seconde entre chacune des 4 prises)
        - Les photos sont enregistrées puis assemblées verticalement
        - La photo finale est postée sur le net
    Bouton + led effet B&W
    Bout on + led effet Vintage

    Bush button long : quitter l'appli
'''

button = Button(18)

def end():
    camera.close()
    pygame.quit()
    sys.exit(0)

def flash():
    # Simulate the flash
    camera.brightness = 80
    sleep(0.3)
    camera.brightness = 50
    
def shot(num_pic:int=3) -> list:
    now = datetime.now()
    picture_name = now.strftime('%d_%m_%H_%M_%S')
    pictures = ['{}_{}.jpeg'.format(picture_name, i) for i in range(num_pic)]

    for pic in pictures:
        flash() 
        camera.capture(pic)
        sleep(1)

    combine(pictures)

def combine(files):
    result = Image.new("RGB", (420, 790))

    for index, file in enumerate(files):
        path = os.path.expanduser(file)
        img = Image.open(path)
        img.thumbnail((400, 400), Image.ANTIALIAS)
        w, h = img.size
        x = 10
        y = 10 + index * 260
        print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
        result.paste(img, (x, y, x + w, y + h))

    result.save(os.path.expanduser('image.jpeg'))


camera = picamera.PiCamera()
camera.rotation = 180

# By default, the resolution is the display resolution.
# camera.resolution = (2592, 1944)
#camera.preview.fullscreen = True
#camera.preview.window = (0, 0, 640, 480)
##try:
##    camera.start_preview()
##    camera.annotate_text = "Hello world!"
##    sleep(10)
##    camera.stop_preview()
##finally:
##    camera.close()


# Capturer une séquence
# import time
# import picamera
# with picamera.PiCamera() as camera:
#     camera.start_preview()
#     time.sleep(2)
#     camera.capture_sequence([
#         'image1.jpg',
#         'image2.jpg',
#         'image3.jpg',
#         'image4.jpg',
#         ])
#     camera.stop_preview()

camera.start_preview()

while True:
    if button.is_pressed:
        camera.annotate_text = "3"
        sleep(1)
        camera.annotate_text = "2"
        sleep(1)
        camera.annotate_text = "1"
        sleep(1)
        print("Pressed")
        shot()
        camera.stop_preview()
    else:
        print("Released")
    sleep(1)

camera.stop_preview()

# Combine 4 images in one
# import os


# files = [
#   '~/Downloads/1.jpg',
#   '~/Downloads/2.jpg',
#   '~/Downloads/3.jpg',
#   '~/Downloads/4.jpg']

