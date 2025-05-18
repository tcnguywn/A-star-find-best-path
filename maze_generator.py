import random

# def generate_maze(grid):
#     for row in grid.cells:
#         for cell in row:
#             cell.set_wall(True)
#
#     start = grid.start
#     stack = [start]
#     start.set_wall(False)
#
#     while stack:
#         current = stack[-1]
#         neighbors = []
#
#         directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
#         for dx, dy in directions:
#             r = current.row + dy
#             c = current.col + dx
#             if 0 <= r < grid.rows and 0 <= c < grid.cols:
#                 neighbor = grid.cells[r][c]
#                 if neighbor.is_wall:
#                     neighbors.append(neighbor)
#
#         if neighbors:
#             chosen = random.choice(neighbors)
#             mid_row = (current.row + chosen.row) // 2
#             mid_col = (current.col + chosen.col) // 2
#             grid.cells[mid_row][mid_col].set_wall(False)
#             chosen.set_wall(False)
#             stack.append(chosen)
#         else:
#             stack.pop()


def generate_maze(grid, wall_probability=0.25):
    for row in grid.cells:
        for cell in row:
            # Đặt tường ngẫu nhiên theo xác suất, tránh start và end
            if cell != grid.start and cell != grid.end:
                if random.random() < wall_probability:
                    cell.set_wall(True)
                else:
                    cell.set_wall(False)
