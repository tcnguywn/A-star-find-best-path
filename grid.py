import pygame
from config import *
class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cell_size = min(AVAILABLE_WIDTH // cols, WINDOW_HEIGHT // rows)
        self.width = self.cell_size * cols
        self.height = self.cell_size * rows
        self.cells = [[Cell(r, c, self.cell_size) for c in range(cols)] for r in range(rows)]
        self.start = self.cells[0][0]
        self.end = self.cells[rows - 1][cols - 1]
        self.start.is_start = True
        self.end.is_end = True
        self.start.color = RED
        self.end.color = GREEN

    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)

    def handle_click(self, pos, is_wall):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            cell = self.cells[row][col]
            if not cell.is_start and not cell.is_end:
                cell.set_wall(is_wall)

    def clear(self):
        for row in self.cells:
            for cell in row:
                cell.set_wall(False)
                if not cell.is_start and not cell.is_end:
                    cell.color = WHITE

    def reset_colors(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_wall and not cell.is_start and not cell.is_end:
                    cell.color = WHITE

    def set_start(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.start.is_start = False
            self.start.color = WHITE
            self.start = self.cells[row][col]
            self.start.is_start = True
            self.start.color = RED

    def set_end(self, pos):
        x, y = pos
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.end.is_end = False
            self.end.color = WHITE
            self.end = self.cells[row][col]
            self.end.is_end = True
            self.end.color = GREEN

class Cell:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.color = WHITE

    def draw(self, screen):
        rect = pygame.Rect(self.col * self.size, self.row * self.size, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, GREY, rect, 1)

    def set_wall(self, value):
        self.is_wall = value
        self.color = BLACK if value else WHITE
