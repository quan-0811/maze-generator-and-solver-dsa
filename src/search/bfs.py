import pygame
from config import *
from typing import List
from cell import Cell
from utils import draw_text_of_running_alg, reconstruct_path, draw_button

def solve_maze_BFS(grid_cells: List[Cell], sc: pygame.Surface):
    """
    Solve the maze using Breadth-First Search (BFS).

    The function performs BFS to explore all possible paths from the starting cell (first element in 
    grid_cells) to the destination cell (last element in grid_cells). It visualizes the search process
    by updating the display (using pygame) as the search progresses, and once the destination is reached, 
    the function reconstructs and returns the path from start to destination.

    Args:
    - grid_cells (List[Cell]): A list of all the cells in the maze, each cell is an object with properties
      such as neighbors, visited status, and methods to check neighbors and draw itself.
    - sc (pygame.Surface): The pygame screen surface used for drawing the maze and visualizing the search 
      process.

    Returns:
    - path (List[Cell]): the path from the starting point of the maze to the destination cell else None
    - visited_cells_count (int): The total number of cells visited during the search.
    """
    # Define the start and destination cells
    start_cell = grid_cells[0]
    destination_cell = grid_cells[-1]

    # Initialize needed structures for BFS and path reconstucting
    queue = []
    visited = set()
    parent = {}
    queue.append(start_cell)
    visited.add(start_cell)
    parent[start_cell] = None

    # Counter to track number of visited cells
    visited_cells_count = 0

    # Main BFS loop
    while queue:
        # Dequeue the first cell and mark it as visited
        current_cell = queue.pop(0)
        current_cell.visited = True
        visited_cells_count += 1

        # Delay for visualization purposes
        pygame.time.delay(60) 
        pygame.display.flip()

        # Redraw the entire maze on each iteration to keep all cells visible
        for cell in grid_cells:
            cell.draw(sc)

        # Display current state of the algorithm
        draw_text_of_running_alg(sc, "RUNNING: BFS", FONT, 17, 20, 230, "#FFFFFF")
        draw_text_of_running_alg(sc, "CELLS EXPLORED: " + str(visited_cells_count), FONT, 17, 20, 260, "#FFFFFF")

        # Display buttons
        draw_button(sc, "GENERATE MAZE", 20, 300, BUTTON_COLOR)
        draw_button(sc, "BFS", 20, 400, BUTTON_COLOR)
        draw_button(sc, "DFS", 20, 350, BUTTON_COLOR)
        draw_button(sc, "BIDIRECTIONAL BFS", 20, 450, BUTTON_COLOR)
        draw_button(sc, "A STAR", 20, 500, BUTTON_COLOR)
        draw_button(sc, "GBFS", 20, 550, BUTTON_COLOR)

        # Draw the visited cell
        current_cell.draw(sc)

        # Check if the current cell is the destination
        if current_cell == destination_cell:
            # If destination is reached, reconstruct and return the path
            path = reconstruct_path(sc, parent, start_cell, destination_cell)
            return path, visited_cells_count

        # Check neighbors and expand the BFS search
        neighbors = current_cell.check_neighbors_for_search(grid_cells)
        for neighbor in neighbors:
            if neighbor not in visited:
                # Enqueue the neighbor for later exploration
                queue.append(neighbor)
                # Mark neighbor as visited
                visited.add(neighbor)
                # Set current cell as the parent of this neighbor
                parent[neighbor] = current_cell 
    
    return None, visited_cells_count
