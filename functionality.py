import pygame
import json

class Button:
    font_size = 30
    rect_color = (200, 200, 200)
    text_color = (0, 0, 0)
    default_color = (200, 200, 200)
    hover_color = (255, 255, 255)
    click_color = (255, 0, 0)
    rect_height = 50

    def __init__(self, text, position, callback_func, screen, FPS):
        self.text = text
        self.position = position
        self.rect_width = len(self.text) * 18
        self.rect_x = self.position[0] - self.rect_width * 0.5
        self.rect_y = self.position[1] - self.rect_height * 0.45
        self.clicked = False
        self.callback_func = callback_func
        self.screen = screen
        self.FPS = FPS

    def draw(self):
        rect = pygame.Rect(self.rect_x, self.rect_y, self.rect_width, self.rect_height)
        pygame.draw.rect(self.screen, self.rect_color, rect)
        draw_text(screen=self.screen, text=self.text, position=self.position)
        if self.clicked:
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (self.rect_x, self.rect_y + self.rect_height),
                (self.rect_x + self.rect_width, self.rect_y + self.rect_height),
                5,
            )


    def hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if (
            self.rect_x < mouse_pos[0] < self.rect_x + self.rect_width
            and self.rect_y < mouse_pos[1] < self.rect_y + self.rect_height
        ):
            self.rect_color = self.hover_color
        else:
            self.rect_color = self.default_color

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if (
            self.rect_x < mouse_pos[0] < self.rect_x + self.rect_width
            and self.rect_y < mouse_pos[1] < self.rect_y + self.rect_height
        ):
            self.clicked = True
            self.callback_func(screen=self.screen, FPS=self.FPS)


def draw_text(
    screen: pygame.Surface,
    size: int = 30,
    text: str = "Hola",
    color: tuple = (0, 0, 0),
    position: tuple = (0, 0),
):
    text_font = pygame.font.Font("resources/Unitblock-JpJma.ttf", size)
    text = text_font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = position
    screen.blit(text, text_rect)


def splash_screen(screen: pygame.Surface, FPS: int):
    app_running = True
    clock = pygame.time.Clock()
    counter = 0
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                app_running = False

        splash = pygame.image.load("assets/bg.png")
        screen.blit(splash, (0, 0))
        draw_text(
            size=50,
            text="Know your",
            color=(255, 255, 255),
            position=(630, 210),
            screen=screen,
        )
        draw_text(
            size=150,
            text="Solar System",
            color=(255, 255, 255),
            position=(680, 300),
            screen=screen,
        )
        if counter < 1 * FPS:
            draw_text(
                size=50,
                text="Press any key to continue",
                color=(200, 200, 200),
                position=(650, 500),
                screen=screen,
            )
        if counter > 1.5 * FPS:
            counter = 0
        counter += 1

        dt = clock.tick(FPS)
        pygame.display.flip()


def menu(screen: pygame.Surface, FPS: int):
    app_running = True
    clock = pygame.time.Clock()
    compare_size_button = Button(text="Compare Size", position=(400, 50), callback_func=compare_size, screen=screen, FPS=FPS)

    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                compare_size_button.click()

        screen.fill((255, 255, 0))
        compare_size_button.hover()
        compare_size_button.draw()

        dt = clock.tick(FPS)
        pygame.display.flip()

def compare_size_planets(left: str, right: str, counter: int, screen: pygame.Surface):
    with open('data.json', 'r') as f:
        data = json.load(f)
    left_planet_radius = data[left]['radius']
    right_planet_radius = data[right]['radius']
    left_planet_volume = (4/3)*(3.14)*(left_planet_radius**3)
    right_planet_volume = (4/3)*(3.14)*(right_planet_radius**3)
    ratio_volume = left_planet_volume / right_planet_volume
    ratio_radius = left_planet_radius / right_planet_radius
    # ratio_radius = 0.5
    # ratio_volume = ratio_radius**3

    left_img = pygame.image.load(f"earth/earth0{counter:03}.jpg")
    right_img = pygame.image.load(f"earth/earth0{counter:03}.jpg")
    if ratio_radius < 1:
        left_img = pygame.transform.scale(left_img, (640*ratio_radius, 640*ratio_radius))
        screen.blit(left_img, (320*(1-ratio_radius), 320*(1-ratio_radius)))
        screen.blit(right_img, (640, 0))
        info_text = f'1 {right} can fit {1/ratio_volume} {left}'
    elif ratio_radius > 1:
        screen.blit(left_img, (0, 0))
        right_img = pygame.transform.scale(right_img, (640/ratio_radius, 640/ratio_radius))
        screen.blit(right_img, (960 - 320/ratio_radius, 320 - 320/ratio_radius))
        info_text = f'1 {left} can fit {ratio_volume} {left}'

    else:
        screen.blit(left_img, (0, 0))
        screen.blit(right_img, (640, 0))
        info_text = f'1 {left} can fit exactly 1 {left} (ROFL)'
    draw_text(size=40, text=info_text, color=(255, 255, 255), position=(640, 660), screen=screen)
    draw_text(
            size=30,
            text=left.capitalize(),
            color=(255, 255, 255),
            position=(320, 320),
            screen=screen,
        )
    draw_text(
            size=30,
            text=right.capitalize(),
            color=(255, 255, 255),
            position=(960, 320),
            screen=screen,
        )

def decrement_index(screen, FPS, left_index):
    print(True)
    # if ind > 1:
    #     return ind -1
    # return ind 



def compare_size(screen: pygame.Surface, FPS: int):
    app_running = True
    clock = pygame.time.Clock()
    left_index = 3
    right_index = 3
    def decrement_index_left(screen, FPS):
        nonlocal left_index
        if left_index > 0:
            left_index -= 1
    def decrement_index_right(screen, FPS):
        nonlocal right_index
        if right_index > 0:
            right_index -= 1
    def increment_index_left(screen, FPS):
        nonlocal left_index
        if left_index < 8:
            left_index += 1
    def increment_index_right(screen, FPS):
        nonlocal right_index
        if right_index < 8:
            right_index += 1
    back = Button(text="<-- Back", position=(80, 35), callback_func=menu, screen=screen, FPS=FPS)
    left_up = Button(text='up', position=(320, 250), callback_func=decrement_index_left, screen=screen, FPS=FPS)
    right_up = Button(text='up', position=(960, 250), callback_func=decrement_index_right, screen=screen, FPS=FPS)
    left_down = Button(text='down', position=(320, 400), callback_func=increment_index_left, screen=screen, FPS=FPS)
    right_down = Button(text='down', position=(960, 400), callback_func=increment_index_right, screen=screen, FPS=FPS)
    counter = 1
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                back.click()
                left_up.click()
                right_up.click()
                left_down.click()
                right_down.click()

        screen.fill((0,0,0))
        bodies = ['sun', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        
        compare_size_planets(left=bodies[left_index], right=bodies[right_index], counter=counter, screen=screen)
        left_up.hover()
        left_up.draw()
        right_up.hover()
        right_up.draw()
        left_down.hover()
        left_down.draw()
        right_down.hover()
        right_down.draw()
        back.hover()
        back.draw()
        draw_text(
            size=80,
            text="Compare Size",
            color=(255, 255, 255),
            position=(640, 50),
            screen=screen,
        )
        
        # pygame.draw.line(screen, (255, 255, 255), (0, 320), (1280, 320), 5)
        # pygame.draw.line(screen, (255, 255, 255), (320, 0), (320, 720), 5)
        # pygame.draw.line(screen, (255, 255, 255), (960, 0), (960, 720), 5)
        counter += 1
        if counter > 240:
            counter = 1

        dt = clock.tick(FPS)
        pygame.display.flip()

