import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont("Arial", 18)
        self.color = GREY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        label = self.font.render(self.text, True, BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.font = pygame.font.SysFont("Arial", 18)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        txt_surface = self.font.render(self.text, True, BLACK)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_value(self):
        try:
            return int(self.text)
        except:
            return None

class ControlPanel:
    def __init__(self, x, width, grid):
        self.x = x
        self.width = width
        self.grid = grid
        self.buttons = []
        self.spacing = 10
        self.button_height = 40

        self.input_box = InputBox(x + self.spacing, 10, width - 2 * self.spacing, 30)
        self.apply_btn = Button(x + self.spacing, 50, width - 2 * self.spacing, self.button_height, "Apply Size", self.apply_size)

    def add_button(self, text, action):
        y = 100 + len(self.buttons) * (self.button_height + self.spacing)
        btn = Button(self.x + self.spacing, y, self.width - 2 * self.spacing, self.button_height, text, action)
        self.buttons.append(btn)

    def draw(self, screen):
        pygame.draw.rect(screen, (230, 230, 230), pygame.Rect(self.x, 0, self.width, WINDOW_HEIGHT))
        pygame.draw.rect(screen, BLACK, pygame.Rect(self.x, 0, self.width, WINDOW_HEIGHT), 2)
        self.input_box.draw(screen)
        self.apply_btn.draw(screen)
        for btn in self.buttons:
            btn.draw(screen)

    def handle_event(self, event):
        self.input_box.handle_event(event)
        self.apply_btn.handle_event(event)
        for btn in self.buttons:
            btn.handle_event(event)

    def apply_size(self):
        val = self.input_box.get_value()
        if val and 5 <= val <= 100:
            self.grid.__init__(val, val)
