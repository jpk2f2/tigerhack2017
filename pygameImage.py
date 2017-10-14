import os
import pygame.camera
import time
import pygame.image
def takePic():
    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()
    img = cam.get_image()
    pygame.image.save(img, "../testPic/photo.bmp")
    os.chdir('/home/david/testPic')
    time.sleep(.1)
    os.system('git init')
    time.sleep(.1)
    os.system('git add photo.bmp')
    time.sleep(.1)
    os.system('git commit -m "new image"')
    time.sleep(.2)
    os.system('git push origin master')
    pygame.camera.quit()
    
