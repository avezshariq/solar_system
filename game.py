from functionality import *
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Solar System')
FPS = 24

# splash_screen(screen=screen, FPS=FPS)
# menu(screen=screen, FPS=FPS)
# speed_of_revolution(screen=screen, FPS=FPS)
year_time(screen=screen, FPS=FPS)

pygame.quit()
