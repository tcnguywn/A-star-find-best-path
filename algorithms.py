import pygame
import time
from config import YELLOW, ORANGE, PURPLE
from itertools import count
from queue import PriorityQueue

def bfs(grid):
    queue = [grid.start]
    visited = set()
    parent = {}
    visited.add(grid.start)
    expanded = 0

    while queue:
        current = queue.pop(0)
        expanded += 1
        if current == grid.end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited and not neighbor.is_wall:
                visited.add(neighbor)
                parent[neighbor] = current
                neighbor.color = YELLOW
                queue.append(neighbor)
        draw_and_delay(grid)

    return reconstruct_path(parent, grid, expanded)

def dfs(grid):
    stack = [grid.start]
    visited = set()
    parent = {}
    visited.add(grid.start)
    expanded = 0

    while stack:
        current = stack.pop()
        expanded += 1
        if current == grid.end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited and not neighbor.is_wall:
                visited.add(neighbor)
                parent[neighbor] = current
                neighbor.color = YELLOW
                stack.append(neighbor)
        draw_and_delay(grid)

    return reconstruct_path(parent, grid, expanded)

def dijkstra(grid):
    pq = PriorityQueue()
    counter = count()
    pq.put((0, next(counter), grid.start))
    parent = {}
    dist = {grid.start: 0}
    expanded = 0

    while not pq.empty():
        _, _, current = pq.get()
        expanded += 1
        if current == grid.end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor.is_wall:
                continue
            new_dist = dist[current] + 1
            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                pq.put((new_dist, next(counter), neighbor))
                parent[neighbor] = current
                neighbor.color = YELLOW
        draw_and_delay(grid)

    return reconstruct_path(parent, grid, expanded)

def astar(grid):
    pq = PriorityQueue()
    counter = count()
    pq.put((0, next(counter), grid.start))
    parent = {}
    g_score = {grid.start: 0}
    f_score = {grid.start: heuristic(grid.start, grid.end)}
    expanded = 0

    while not pq.empty():
        _, _, current = pq.get()
        expanded += 1

        if current == grid.end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor.is_wall:
                continue
            tentative = g_score[current] + 1
            if neighbor not in g_score or tentative < g_score[neighbor]:
                g_score[neighbor] = tentative
                f_score[neighbor] = tentative + heuristic(neighbor, grid.end)
                pq.put((f_score[neighbor], next(counter), neighbor))
                parent[neighbor] = current
                neighbor.color = YELLOW
        draw_and_delay(grid)

    return reconstruct_path(parent, grid, expanded)

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def get_neighbors(grid, cell):
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    result = []
    for dr, dc in dirs:
        r, c = cell.row + dr, cell.col + dc
        if 0 <= r < grid.rows and 0 <= c < grid.cols:
            result.append(grid.cells[r][c])
    return result

def reconstruct_path(parent, grid, expanded):
    current = grid.end
    length = 0
    while current in parent:
        current = parent[current]
        if not current.is_start:
            current.color = PURPLE
        draw_and_delay(grid)
        length += 1
    return {"length": length, "expanded": expanded}

def draw_and_delay(grid):
    screen = pygame.display.get_surface()
    screen.fill((255, 255, 255))
    grid.draw(screen)
    pygame.display.flip()
    pygame.time.delay(20)
