import pygame

# Decorator function
def update_and_quit(func):
    def wrapper(*args, **kwargs):
        clock = pygame.time.Clock()
        app_running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False
        dt = clock.tick(24)
        a = func(app_running, *args, **kwargs)
        pygame.display.flip()   
        return a
    return wrapper



@update_and_quit
def splash_screen(app_running, screen):
    splash_running  = True
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                splash_running = False
    splash = pygame.image.load('assets/bg.png')
    screen.blit(splash, (0, 0))
    solar_system_font = pygame.font.Font('resources/Unitblock-JpJma.ttf', 100)
    solar_system = solar_system_font.render('Solar System', True, (255, 255, 255))
    solar_system_rect = solar_system.get_rect()
    solar_system_rect.center = (640, 300)
    screen.blit(solar_system, solar_system_rect)
    return app_running, splash_running
