import pygame
import time
from config import YELLOW, ORANGE, PURPLE, FRONTIER_COLOR, VISITED_COLOR, PATH_COLOR
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

        if current != grid.start and current != grid.end:
            current.color = FRONTIER_COLOR

        if current == grid.end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited and not neighbor.is_wall:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

                if neighbor != grid.end:
                    neighbor.color = VISITED_COLOR
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

        if current != grid.start and current != grid.end:
            current.color = FRONTIER_COLOR

        if current == grid.end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited and not neighbor.is_wall:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

                if neighbor != grid.end:
                    neighbor.color = VISITED_COLOR
        draw_and_delay(grid)

    return reconstruct_path(parent, grid, expanded)


def dijkstra(grid):
    pq = PriorityQueue()
    counter = count()
    pq.put((0, next(counter), grid.start))
    parent = {}
    dist = {grid.start: 0}
    expanded = 0
    in_queue = set()
    in_queue.add(grid.start)

    while not pq.empty():
        _, _, current = pq.get()
        in_queue.discard(current)
        expanded += 1

        if current != grid.start and current != grid.end:
            current.color = FRONTIER_COLOR

        if current == grid.end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor.is_wall:
                continue
            new_dist = dist[current] + 1
            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = current
                pq.put((new_dist, next(counter), neighbor))
                in_queue.add(neighbor)

                if neighbor != grid.end:
                    neighbor.color = VISITED_COLOR
        draw_and_delay(grid)

    return reconstruct_path(parent, grid, expanded)


def astar(grid):

    pq = PriorityQueue()
    counter = count()

    g_score = {grid.start: 0}
    f_score = {grid.start: heuristic(grid.start, grid.end)}
    parent = {}

    pq.put((f_score[grid.start], next(counter), grid.start))
    expanded = 0
    open_set = {grid.start}

    while not pq.empty():
        _, _, current = pq.get()
        open_set.discard(current)
        expanded += 1

        if current != grid.start and current != grid.end:
            current.color = FRONTIER_COLOR  # node tốt nhất đang xét

        if current == grid.end:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor.is_wall:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, grid.end)
                parent[neighbor] = current
                pq.put((f_score[neighbor], next(counter), neighbor))
                open_set.add(neighbor)

                if neighbor != grid.end:
                    neighbor.color = VISITED_COLOR  # các node hàng xóm được mở rộng

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
            current.color = PATH_COLOR
        draw_and_delay(grid)
        length += 1
    return {"length": length, "expanded": expanded}

def draw_and_delay(grid):
    screen = pygame.display.get_surface()
    screen.fill((255, 255, 255))
    grid.draw(screen)
    pygame.display.flip()
    pygame.time.delay(20)
