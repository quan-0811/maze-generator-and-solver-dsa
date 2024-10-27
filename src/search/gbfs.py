import pygame
import heapq  # For priority queue functionality
from typing import List
from cell import Cell
from config import *
from utils import manhattan_distance, reconstruct_path, draw_text_of_running_alg, draw_button

def solve_maze_greedy_bfs(grid_cells: List[Cell], sc: pygame.Surface):
    """
    Solve the maze using the Greedy Best-First Search (GBFS) algorithm, which selects the next cell 
    to explore based on the heuristic value (Manhattan distance) to the destination.

    Args:
    - grid_cells (List[Cell]): List of all grid cells in the maze.
    - sc (pygame.Surface): The screen surface for drawing the maze.

    Returns:
    - path (List[Cell]): The reconstructed path from the start to the destination if found, else None.
    - visited_cells_count (int): The total number of cells visited during the search.
    """

    # Define the start end destination cells
    start_cell = grid_cells[0]
    destination_cell = grid_cells[-1]

    # Priority queue to keep track of cells to explore, ordered by heuristic cost (h_cost) (holds tuples of (h_cost, id, cell))
    open_set = []
    heapq.heappush(open_set, (0, id(start_cell), start_cell))

    # Visited set and parent dictionary for path reconstruction
    parent = {}
    parent[start_cell] = None
    visited = set()

    # Counter to track number of visited cells
    visited_cells_count = 0

    # Main GBFS loop
    while open_set:
        # Get the cell with the lowest heuristic (h_cost) and mark it as visited
        _, _, current_cell = heapq.heappop(open_set)
        current_cell.visited = True
        visited_cells_count += 1

        # If we reached the destination, reconstruct the path
        if current_cell == destination_cell:
            path = reconstruct_path(sc, parent, start_cell, destination_cell)
            return path, visited_cells_count

        # Redraw the entire maze to show progress
        for cell in grid_cells:
            cell.draw(sc)
        current_cell.draw(sc)

        # Display the current state of the algorithm
        draw_text_of_running_alg(sc, "RUNNING: GBFS", FONT, 17, 20, 230, "#FFFFFF")
        draw_text_of_running_alg(sc, "CELLS EXPLORED: " + str(visited_cells_count), FONT, 17, 20, 260, "#FFFFFF")

        # Display buttons
        draw_button(sc, "GENERATE MAZE", 20, 300, BUTTON_COLOR)
        draw_button(sc, "BFS", 20, 400, BUTTON_COLOR)
        draw_button(sc, "DFS", 20, 350, BUTTON_COLOR)
        draw_button(sc, "BIDIRECTIONAL BFS", 20, 450, BUTTON_COLOR)
        draw_button(sc, "A STAR", 20, 500, BUTTON_COLOR)
        draw_button(sc, "GBFS", 20, 550, BUTTON_COLOR)

        # Delay for visualization purposes
        pygame.time.delay(60)
        pygame.display.flip()

        # Mark the current cell as visited
        visited.add(current_cell)

        # Get the neighbors of the current cell
        neighbors = current_cell.check_neighbors_for_search(grid_cells)
        for neighbor in neighbors:
            # Skip visited cells
            if neighbor in visited:
                continue

            # This is where Greedy BFS differs from A*: we only use the heuristic (h_cost)
            h_cost = manhattan_distance(neighbor, destination_cell)

            # If neighbor is not in open_set, add it with its h_cost
            if neighbor not in [item[2] for item in open_set]:
                parent[neighbor] = current_cell
                heapq.heappush(open_set, (h_cost, id(neighbor), neighbor))

    return None, visited_cells_count


