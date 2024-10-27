import pygame
from cell import Cell
from typing import List
from config import *
from utils import draw_text_of_running_alg, reconstruct_path, draw_button

def solve_maze_DFS(grid_cells: List[Cell], sc: pygame.Surface):
    """
    Solve the maze using Depth-First Search (DFS), which explores as far as possible
    along each branch before backtracking. DFS uses a stack to manage the traversal 
    and explores deeper into the maze with each step.

    Args:
    - grid_cells (list): A list of all cells in the maze, where each cell is an object 
      with properties like coordinates and neighbors, and methods for drawing and searching.
    - sc (pygame.Surface): The pygame screen surface used for drawing and visualizing 
      the maze and DFS traversal process.

    Returns:
    - path (list or None): A list of cells representing the solution path from the 
      start to the destination if found, otherwise returns None.
    - visited_cells_count (int): The total number of cells visited during the search.
    """

    # Define the start and destination cells
    start_cell = grid_cells[0]
    destination_cell = grid_cells[-1]

    # Initialize needed structures for BFS and path reconstucting later
    stack = []  
    visited = set()  
    parent = {}
    stack.append(start_cell)
    visited.add(start_cell)
    parent[start_cell] = None

    # Inintialize visited cell counter
    visited_cells_count = 0

    # Main DFS loop
    while stack:
        # Pop the top cell from the stack and mark it as visited
        current_cell = stack.pop()
        current_cell.visited = True
        visited_cells_count += 1

        # Delay for visualization purposes
        pygame.time.delay(60) 
        pygame.display.flip()

        # Redraw the entire maze on each iteration to keep all cells visible
        for cell in grid_cells:
            cell.draw(sc)
        
        # Display the current state of the algorithm
        draw_text_of_running_alg(sc, "RUNNING: DFS", FONT, 17, 20, 230, "#FFFFFF")
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

        # Check neighbors and explore deeper
        neighbors = current_cell.check_neighbors_for_search(grid_cells)
        for neighbor in neighbors:
            if neighbor not in visited:
                # Push the neighbor onto the stack
                stack.append(neighbor)
                # Mark the neighbor as visited
                visited.add(neighbor)
                # Set the current cell as the parent of the neighbor
                parent[neighbor] = current_cell
    
    return None, visited_cells_count
