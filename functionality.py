import pygame
import json
import math


def calculate_angle(center, point):
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    return math.degrees(math.atan2(-dy, dx))


class Button:
    font_size = 30
    rect_color = (200, 200, 200)
    text_color = (0, 0, 0)
    default_color = (200, 200, 200)
    hover_color = (255, 255, 255)
    click_color = (255, 0, 0)
    rect_height = 50

    def __init__(
        self,
        text: str,
        position: tuple,
        callback_func,
        screen: pygame.Surface,
        FPS: int,
    ):
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
    counter = 1
    fly_in = True
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                app_running = False

        if fly_in:
            green_x = -700 + 5 * counter
            red_x = 1300 - 5 * counter
            if green_x > -350:
                fly_in = False
        else:
            green_x = -345
            red_x = 945

        screen.fill((0, 0, 0))
        green = pygame.image.load(f"green/green{counter:04}.jpg")
        screen.blit(green, (green_x, 0))
        red = pygame.image.load(f"red/red{counter:04}.jpg")
        screen.blit(red, (red_x, 0))
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
        draw_text(
            size=50,
            text="Press any key to continue",
            color=(220, 220, 220),
            position=(650, 500),
            screen=screen,
        )
        if counter > 239:
            counter = 1
            repeat = True
        counter += 1

        dt = clock.tick(FPS)
        pygame.display.flip()


def menu(screen: pygame.Surface, FPS: int):
    app_running = True
    clock = pygame.time.Clock()
    counter = 1
    compare_size_button = Button(
        text="Compare Size",
        position=(1000, 200),
        callback_func=compare_size,
        screen=screen,
        FPS=FPS,
    )
    compare_rotation_button = Button(
        text="Compare Rotation Speed",
        position=(1000, 300),
        callback_func=compare_rotation,
        screen=screen,
        FPS=FPS,
    )
    speed_of_revolution_button = Button(
        text="Speed of revolution",
        position=(1000, 400),
        callback_func=speed_of_revolution,
        screen=screen,
        FPS=FPS,
    )
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                compare_size_button.click()
                compare_rotation_button.click()
                speed_of_revolution_button.click()

        bg = pygame.image.load(f"green/green{counter:04}.jpg")

        mouse_position = pygame.mouse.get_pos()
        angle = calculate_angle((360, 360), mouse_position)
        rotated_image = pygame.transform.rotate(bg, angle)
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = (360, 360)
        screen.fill((0, 0, 0))
        screen.blit(rotated_image, rotated_rect)
        compare_size_button.hover()
        compare_size_button.draw()
        compare_rotation_button.hover()
        compare_rotation_button.draw()
        speed_of_revolution_button.hover()
        speed_of_revolution_button.draw()
        if counter > 239:
            counter = 1
        counter += 1

        dt = clock.tick(FPS)
        pygame.display.flip()


def compare_size_planets(left: str, right: str, counter: int, screen: pygame.Surface):
    with open("data.json", "r") as f:
        data = json.load(f)
    left_planet_radius = data[left]["radius"]
    right_planet_radius = data[right]["radius"]
    ratio_radius = left_planet_radius / right_planet_radius
    ratio_volume = ratio_radius**3

    left_img = pygame.image.load(f"{left}/{left}0{counter:03}.jpg")
    right_img = pygame.image.load(f"{right}/{right}0{counter:03}.jpg")
    if ratio_radius < 1:
        left_img = pygame.transform.scale(
            left_img, (640 * ratio_radius, 640 * ratio_radius)
        )
        screen.blit(left_img, (320 * (1 - ratio_radius), 320 * (1 - ratio_radius)))
        screen.blit(right_img, (640, 0))
        info_text = f"1 {right} can fit {round(1/ratio_volume, 2)} {left}"

    elif ratio_radius > 1:
        screen.blit(left_img, (0, 0))
        right_img = pygame.transform.scale(
            right_img, (640 / ratio_radius, 640 / ratio_radius)
        )
        screen.blit(right_img, (960 - 320 / ratio_radius, 320 - 320 / ratio_radius))
        info_text = f"1 {left} can fit {round(ratio_volume, 2)} {right}"

    else:
        screen.blit(left_img, (0, 0))
        screen.blit(right_img, (640, 0))
        info_text = f"1 {left} can fit exactly 1 {right} (ROFL)"

    draw_text(
        size=40,
        text=info_text,
        color=(255, 255, 255),
        position=(640, 660),
        screen=screen,
    )
    draw_text(
        size=70,
        text=left.capitalize(),
        color=(100, 100, 100),
        position=(320, 500),
        screen=screen,
    )
    draw_text(
        size=70,
        text=right.capitalize(),
        color=(100, 100, 100),
        position=(960, 500),
        screen=screen,
    )


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

    back = Button(
        text="<-- Back", position=(80, 35), callback_func=menu, screen=screen, FPS=FPS
    )
    left_up = Button(
        text="up",
        position=(320, 250),
        callback_func=decrement_index_left,
        screen=screen,
        FPS=FPS,
    )
    right_up = Button(
        text="up",
        position=(960, 250),
        callback_func=decrement_index_right,
        screen=screen,
        FPS=FPS,
    )
    left_down = Button(
        text="down",
        position=(320, 400),
        callback_func=increment_index_left,
        screen=screen,
        FPS=FPS,
    )
    right_down = Button(
        text="down",
        position=(960, 400),
        callback_func=increment_index_right,
        screen=screen,
        FPS=FPS,
    )
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

        screen.fill((0, 0, 0))
        bodies = [
            "sun",
            "mercury",
            "venus",
            "earth",
            "mars",
            "jupiter",
            "saturn",
            "uranus",
            "neptune",
        ]
        compare_size_planets(
            left=bodies[left_index],
            right=bodies[right_index],
            counter=counter,
            screen=screen,
        )
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
        counter += 1
        if counter > 240:
            counter = 1

        dt = clock.tick(FPS)
        pygame.display.flip()


def compare_rotation(screen: pygame.Surface, FPS: int):
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

    back = Button(
        text="<-- Back", position=(80, 35), callback_func=menu, screen=screen, FPS=FPS
    )
    left_up = Button(
        text="up",
        position=(320, 250),
        callback_func=decrement_index_left,
        screen=screen,
        FPS=FPS,
    )
    right_up = Button(
        text="up",
        position=(960, 250),
        callback_func=decrement_index_right,
        screen=screen,
        FPS=FPS,
    )
    left_down = Button(
        text="down",
        position=(320, 400),
        callback_func=increment_index_left,
        screen=screen,
        FPS=FPS,
    )
    right_down = Button(
        text="down",
        position=(960, 400),
        callback_func=increment_index_right,
        screen=screen,
        FPS=FPS,
    )
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

        screen.fill((0, 0, 0))
        bodies = [
            "sun",
            "mercury",
            "venus",
            "earth",
            "mars",
            "jupiter",
            "saturn",
            "uranus",
            "neptune",
        ]
        compare_rotation_planets(
            left=bodies[left_index],
            right=bodies[right_index],
            counter=counter,
            screen=screen,
        )
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
            text="Rotation Speed",
            color=(255, 255, 255),
            position=(640, 50),
            screen=screen,
        )
        counter += 1
        if counter > 240:
            counter = 1

        dt = clock.tick(FPS)
        pygame.display.flip()


def compare_rotation_planets(
    left: str, right: str, counter: int, screen: pygame.Surface
):
    with open("data.json", "r") as f:
        data = json.load(f)
    left_planet_hours = data[left]["rotation_time_hours"]
    right_planet_hours = data[right]["rotation_time_hours"]
    ratio_speed = left_planet_hours / right_planet_hours
    if ratio_speed > 40:
        ratio_speed = 40
    if ratio_speed < 0.025:
        ratio_speed = 0.025

    slow_color = (0, 0, 255)
    fast_color = (255, 0, 0)
    if ratio_speed < 1:
        right_counter = counter
        left_counter = int(counter / ratio_speed)
        if left_counter > 240:
            left_counter = 240
        left_color = fast_color
        right_color = slow_color
    elif ratio_speed > 1:
        left_counter = counter
        right_counter = int(ratio_speed * counter)
        if right_counter > 240:
            right_counter = 240
        left_color = slow_color
        right_color = fast_color
    else:
        left_counter = right_counter = counter
        left_color = right_color = slow_color

    left_img = pygame.image.load(f"{left}/{left}0{left_counter:03}.jpg")
    right_img = pygame.image.load(f"{right}/{right}0{right_counter:03}.jpg")
    screen.blit(left_img, (0, 0))
    screen.blit(right_img, (640, 0))

    draw_text(
        size=70,
        text=f"{left.capitalize()} ({left_planet_hours})",
        color=(100, 100, 100),
        position=(320, 500),
        screen=screen,
    )
    draw_text(
        size=70,
        text=f"{right.capitalize()} ({right_planet_hours})",
        color=(100, 100, 100),
        position=(960, 500),
        screen=screen,
    )
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (80, 680),
        (560, 680),
        10,
    )
    pygame.draw.line(
        screen,
        left_color,
        (80, 680),
        (80 + 2 * left_counter, 680),
        10,
    )
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (720, 680),
        (1200, 680),
        10,
    )
    pygame.draw.line(
        screen,
        right_color,
        (720, 680),
        (720 + 2 * right_counter, 680),
        10,
    )

def speed_of_revolution(screen:pygame.Surface, FPS:int):
    with open('data.json', 'r') as f:
        data = json.load(f)
    app_running = True
    race = 1
    clock = pygame.time.Clock()
    bodies = [
            "mercury",
            "venus",
            "earth",
            "mars",
            "jupiter",
            "saturn",
            "uranus",
            "neptune",
        ]
    counter = 1
    back = Button(
        text="<-- Back", position=(80, 35), callback_func=menu, screen=screen, FPS=FPS
    )
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                back.click()

        screen.fill((0, 0, 0))
        back.hover()
        back.draw()
        draw_text(screen=screen, size=80, text='Speed of Revolution', color=(255, 255, 255), position=(640, 40))
        for ind, body in enumerate(bodies):
            img = pygame.image.load(f"{body}/{body}0{counter:03}.jpg")
            scaled_img = pygame.transform.scale(
            img, (80, 80)
            )
            speed = data[body]['speed_of_revolution_km_per_s']
            draw_text(screen=screen, size=30, text=body, color=(100, 100, 100), position=(-50+speed*race*0.3, 120 + ind*80))
            screen.blit(scaled_img, (speed*race*0.3, 80 + ind*80))
            if speed*race*0.3 > 1280:
                draw_text(screen=screen, size=30, text=f'{speed}Km/s', color=(255, 255, 255), position=(640, 120+ind*80))

        if counter > 239:
            counter = 1
        counter += 1
        if race > 800:
            race = 1
        race += 1
        dt = clock.tick(FPS)
        pygame.display.flip()


def year_time(screen: pygame.Surface, FPS: int):
    app_running = True
    clock = pygame.time.Clock()
    left_index = 2
    right_index = 2

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
        if left_index < 7:
            left_index += 1

    def increment_index_right(screen, FPS):
        nonlocal right_index
        if right_index < 7:
            right_index += 1

    back = Button(
        text="<-- Back", position=(80, 35), callback_func=menu, screen=screen, FPS=FPS
    )
    left_up = Button(
        text="up",
        position=(320, 200),
        callback_func=decrement_index_left,
        screen=screen,
        FPS=FPS,
    )
    right_up = Button(
        text="up",
        position=(960, 200),
        callback_func=decrement_index_right,
        screen=screen,
        FPS=FPS,
    )
    left_down = Button(
        text="down",
        position=(320, 450),
        callback_func=increment_index_left,
        screen=screen,
        FPS=FPS,
    )
    right_down = Button(
        text="down",
        position=(960, 450),
        callback_func=increment_index_right,
        screen=screen,
        FPS=FPS,
    )
    counter = 1
    rev = 0
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

        screen.fill((0, 0, 0))
        bodies = [
            "mercury",
            "venus",
            "earth",
            "mars",
            "jupiter",
            "saturn",
            "uranus",
            "neptune",
        ]
        year_time_planets(
            left=bodies[left_index],
            right=bodies[right_index],
            counter=counter,
            screen=screen,
            rev=rev
        )
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
            text="Year length",
            color=(255, 255, 255),
            position=(640, 50),
            screen=screen,
        )
        counter += 1
        if counter > 240:
            counter = 1
        rev += 1
        if rev > 360:
            rev = 0

        dt = clock.tick(FPS)
        pygame.display.flip()



def year_time_planets(
    left: str, right: str, counter: int, screen: pygame.Surface, rev: int
):
    with open("data.json", "r") as f:
        data = json.load(f)
    left_planet_days = data[left]["time_for_one_year_days"]
    right_planet_days = data[right]["time_for_one_year_days"]
    ratio_days = left_planet_days / right_planet_days


    slow_color = (0, 0, 255)
    fast_color = (255, 0, 0)
    if ratio_days < 1:
        right_radians = rev*math.pi/180
        left_radians = right_radians/ratio_days
        left_color, right_color = fast_color, slow_color
    elif ratio_days > 1:
        left_radians = rev*math.pi/180
        right_radians = left_radians*ratio_days
        left_color, right_color = slow_color, fast_color
    else:
        left_radians = right_radians = rev*math.pi/180
        left_color, right_color = slow_color, slow_color

    left_radians *= -1
    right_radians *= -1

    left_x = math.cos(left_radians)
    left_y = math.sin(left_radians)
    right_x = math.cos(right_radians)
    right_y = math.sin(right_radians)

    left_img = pygame.image.load(f"{left}/{left}0{counter:03}.jpg")
    right_img = pygame.image.load(f"{right}/{right}0{counter:03}.jpg")
    left_img = pygame.transform.scale(left_img, (50, 50))
    right_img = pygame.transform.scale(right_img, (50, 50))

    left_rect = pygame.Rect(70, 70, 500, 500)
    pygame.draw.arc(screen, left_color, left_rect, 0, -1*left_radians, math.floor(-1*left_radians/6.26) + 1)
    screen.blit(left_img, (295 + 250*left_x, 295 + 250*left_y))

    right_rect = pygame.Rect(710, 70, 500, 500)
    pygame.draw.arc(screen, right_color, right_rect, 0, -1*right_radians, math.floor(-1*right_radians/6.26) + 1)
    screen.blit(right_img, (935 + 250*right_x, 295 + 250*right_y))

    sun_img = pygame.image.load(f"sun/sun0{counter:03}.jpg")
    sun_img = pygame.transform.scale(sun_img, (100, 100))
    screen.blit(sun_img, (270, 270))
    screen.blit(sun_img, (910, 270))

    draw_text(
        size=40,
        text=f"{left.capitalize()} ({round(-1*left_radians/6.28, 1)} years)",
        color=(200, 200, 200),
        position=(320, 680),
        screen=screen,
    )
    draw_text(
        size=40,
        text=f"{right.capitalize()} ({round(-1*right_radians/6.28, 1)} years)",
        color=(200, 200, 200),
        position=(960, 680),
        screen=screen,
    )