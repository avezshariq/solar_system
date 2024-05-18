import pygame
import random


class Button:
    font_size = 30
    rect_color = (200, 200, 200)
    text_color = (0, 0, 0)
    default_color = (200, 200, 200)
    hover_color = (255, 255, 255)
    click_color = (255, 0, 0)
    rect_height = 60

    def __init__(self, text, position):
        self.text = text
        self.position = position
        self.rect_width = len(self.text) * 12
        self.rect_x = self.position[0] - self.rect_width / 2
        self.rect_y = self.position[1] - self.rect_height / 2
        self.clicked = False

    def draw(self, screen):
        rect = pygame.Rect(self.rect_x, self.rect_y, self.rect_width, self.rect_height)
        pygame.draw.rect(screen, self.rect_color, rect)
        draw_text(screen=screen, text=self.text, position=self.position)
        if self.clicked:
            pygame.draw.line(
                screen,
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

    def click(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if (
            self.rect_x < mouse_pos[0] < self.rect_x + self.rect_width
            and self.rect_y < mouse_pos[1] < self.rect_y + self.rect_height
        ):
            print("I am clicked")
            self.clicked = True


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
    b1 = Button(text="Click here for all the help you need", position=(640, 100))

    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                b1.click(screen)

        screen.fill((255, 255, 0))
        b1.hover()
        b1.draw(screen=screen)

        dt = clock.tick(FPS)
        pygame.display.flip()
