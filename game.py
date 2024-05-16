from functionality import *
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Solar System')

app_running = True
while app_running:
    splash_running = True
    while splash_running:
        app_running, splash_running = splash_screen(screen)
    

pygame.quit()
