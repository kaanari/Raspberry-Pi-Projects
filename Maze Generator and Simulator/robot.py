import pygame, sys
from pygame.locals import *

def main():
    pygame.init()

    DISPLAY=pygame.display.set_mode((500,400),0,32)

    WHITE=(255,255,255)
    blue=(0,0,255)

    DISPLAY.fill(WHITE)

    pygame.draw.circle(DISPLAY, (0,0,0), (200,157), 7)
    pygame.draw.rect(DISPLAY,(0,0,0),(200,150,14,14))
    pygame.draw.rect(DISPLAY,(255,0,0),(191,156,6,2))
    pygame.draw.rect(DISPLAY,(255,0,0),(198,160,2,6))
    pygame.draw.rect(DISPLAY,(255,0,0),(198,148,2,6))
    pygame.draw.rect(DISPLAY,(0,255,0),(206,148,6,3))
    pygame.draw.rect(DISPLAY,(0,255,0),(206,163,6,3))



    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

main()