import pygame
from pygame.locals import *
import pygame.camera
import sys
import time
#major definitions
DEBUG = True
CAMERA = True # useful for debugging without needing to pull camera....
displayTimer = 1000 #1000 *120 #1000ms * seconds = 2 minutes.


#define and write to a log file
def writeLog():
    #read in count and a log file
    countFile = "count.txt"
    cFile = open(countFile,"r+")
    value = int(cFile.read())
    cFile.seek(0)
    value+=1
    cFile.write(str(value))
    cFile.truncate()
    cFile.close()
    #increment count
    #write to log file in milliseconds since start
    logFile = "log.txt"
    lFile = open(logFile,"a")
    logOutput = "Handheld"+ " "+ str(pygame.time.get_ticks())+','
    lFile.write(logOutput)
    lFile.close()

def main():
    pygame.init()
    pygame.camera.init()
    #Define screen and display size
    displayInfo = pygame.display.Info()
    screen_x = displayInfo.current_w
    screen_y = displayInfo.current_h
    if(DEBUG):
        screen_x = screen_x/2
        screen_y = screen_y/2
        screen = pygame.display.set_mode([screen_x,screen_y])
    else:
        screen = pygame.display.set_mode([screen_x,screen_y],pygame.FULLSCREEN)
    screen.fill((255,255,255))

    #define a rectangle to hold a start dialog 
    rectBG = (0,0,255)
    startRect = pygame.Surface((screen_x,screen_y/3))
    startRect.fill(rectBG)

    #define text on start dialog
    #print(pygame.font.get_fonts())
    font = pygame.font.Font(None,72)
    text = font.render("Touch screen to start.",1,(10,10,10))
    textpos = text.get_rect()
    textpos.centerx = startRect.get_rect().centerx
    textpos.centery = startRect.get_rect().centery
    startRect.blit(text,textpos)

    #define camera
    if(CAMERA):
        cameraList = pygame.camera.list_cameras()
        camera = pygame.camera.Camera(cameraList[1])
        camera.start()

    displayDialog = True
    while True:
        
        for event in pygame.event.get():
            if(event.type == KEYDOWN):
                if(event.key == K_q):
                    #pygame.quit()
                    exit()
            if(event.type == pygame.QUIT):
                exit()
            if(event.type == MOUSEBUTTONDOWN and displayDialog == True):
                displayDialog = False
                #collect stats;
                writeLog()
                pygame.time.set_timer(USEREVENT,displayTimer)
            if(event.type == USEREVENT):
                displayDialog = True;
        if(CAMERA):
            screen.blit(pygame.transform.scale(camera.get_image(),(screen_x,screen_y)),(0,0))
        else:
            screen.fill((255,255,255))
        if(displayDialog):
            screen.blit(startRect,(0,screen_y/3))
        pygame.display.update()
main()