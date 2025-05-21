import pygame
from grid import Grid
from algorithms import bfs, dfs, dijkstra, astar
from maze_generator import generate_maze
from control_panel import ControlPanel
from config import *
import matplotlib.pyplot as plt


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

# Khởi tạo lưới mặc định
grid = Grid(20, 20)
selecting = None

def main():
    global selecting
    clock = pygame.time.Clock()
    running = True
    algorithm = None

    panel = ControlPanel(grid.width, PANEL_WIDTH, grid)
    panel.add_button("Generate Maze", lambda: generate_maze(grid))
    panel.add_button("Set Start", lambda: set_selecting('start'))
    panel.add_button("Set End", lambda: set_selecting('end'))
    panel.add_button("Clear Grid", lambda: grid.clear())
    panel.add_button("Run BFS", lambda: run_algo(bfs, "BFS"))
    panel.add_button("Run DFS", lambda: run_algo(dfs, "DFS"))
    panel.add_button("Dijkstra", lambda: run_algo(dijkstra, "Dijkstra"))
    panel.add_button("Run A*", lambda: run_algo(astar, "A*"))
    panel.add_button("Compare All", run_all_algorithms)

    while running:
        screen.fill(WHITE)
        grid.draw(screen)
        panel.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            panel.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x < grid.width:
                    pos = (x, y)
                    if selecting == 'start':
                        grid.set_start(pos)
                        selecting = None
                    elif selecting == 'end':
                        grid.set_end(pos)
                        selecting = None
                    else:
                        if event.button == 1:
                            grid.handle_click(pos, True)
                        elif event.button == 3:
                            grid.handle_click(pos, False)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    generate_maze(grid)
                elif event.key == pygame.K_c:
                    grid.clear()
                elif event.key == pygame.K_s:
                    selecting = 'start'
                elif event.key == pygame.K_e:
                    selecting = 'end'
                elif event.key == pygame.K_b:
                    algorithm = bfs
                elif event.key == pygame.K_d:
                    algorithm = dfs
                elif event.key == pygame.K_j:
                    algorithm = dijkstra
                elif event.key == pygame.K_a:
                    algorithm = astar
                elif event.key == pygame.K_v:
                    run_all_algorithms()

        if algorithm:
            result = algorithm(grid)
            print_result(result, algorithm.__name__)
            algorithm = None

    pygame.quit()

def run_algo(algo, name):
    grid.reset_colors()
    result = algo(grid)
    if result:
        print(f"{name.upper()} | Path length: {result['length']} | Expanded: {result['expanded']} | Time: {result['time']}")

def run_all_algorithms():
    print("Running all algorithms for comparison...\n")

    algorithms = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("Dijkstra", dijkstra),
        ("A*", astar)
    ]

    results = []

    for name, algo in algorithms:
        grid.reset_colors()
        result = algo(grid)
        if result:
            result["name"] = name
            print_result(result, name)
            results.append(result)

    # Hiển thị biểu đồ sau khi chạy xong
    show_results_chart(results)

def show_results_chart(results):
    names = [r["name"] for r in results]
    lengths = [r["length"] for r in results]
    expanded = [r["expanded"] for r in results]
    times = [r["time"] for r in results]

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.bar(names, lengths, color='skyblue')
    plt.title("Path Length")
    plt.ylabel("Steps")

    plt.subplot(1, 3, 2)
    plt.bar(names, expanded, color='orange')
    plt.title("Expanded Nodes")
    plt.ylabel("Count")

    plt.subplot(1, 3, 3)
    plt.bar(names, times, color='green')
    plt.title("Execution Time")
    plt.ylabel("Seconds")

    plt.suptitle("Pathfinding Algorithm Comparison", fontsize=14)
    plt.tight_layout()
    plt.show()


def print_result(result, name):
    print(f"{name.upper()} | Path length: {result['length']} | Expanded: {result['expanded']} | Time: {result['time']}")

def set_selecting(mode):
    global selecting
    selecting = mode

if __name__ == "__main__":
    main()
