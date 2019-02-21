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
    Bouton mode : B&W -> B&W + Vintage -> Vintage -> Normal -> B&W -> ...
    Bouton last : Affiche la dernière photo

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

    # capture_sequence does the job but doesn't simulate a flash
    # camera.capture_sequence(pictures)

    for pic in pictures:
        flash() 
        camera.capture(pic)
        sleep(1)

    shot = combine(picture_name, pictures)
    loadpic(shot)

def combine(base_name:str, files:list) -> str:
    output_name = '{}.jpeg'.format(base_name)

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

    result.save(os.path.expanduser(output_name))
    return output_name

def loadpic(imageName): # affiche imagename
    print("loading image: " + imageName)
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    background = pygame.image.load(imageName);
    background.convert_alpha()
    background = pygame.transform.scale(background,(width,height))
    screen.blit(background,(0,0),(0,0,width,height))
    pygame.display.flip()
    sleep(2)
    pygame.display.quit()

camera = picamera.PiCamera()
camera.rotation = 180
# camera.resolution = (2592, 1944)
# camera.preview.fullscreen = True
# camera.preview.window = (0, 0, 640, 480)

camera.start_preview()

while True:
    try:
        button.wait_for_press()
        camera.annotate_text = "3"
        sleep(1)
        camera.annotate_text = "2"
        sleep(1)
        camera.annotate_text = "1"
        sleep(1)
        shot()
    except KeyboardInterrupt:
        camera.stop_preview()
        break
