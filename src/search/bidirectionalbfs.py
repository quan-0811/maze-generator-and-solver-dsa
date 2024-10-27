import pygame
from config import *
from cell import Cell
from typing import List
from utils import draw_text_of_running_alg, reconstruct_bidirectional_path, draw_button

def solve_maze_bidirectional_BFS(grid_cells: List[Cell], sc: pygame.Surface):
    """
    Solve the maze using the bidirectional BFS search algorithm, which simultaneously searches 
    from both the start and destination cells. If the searches meet, the path is reconstructed.

    Args:
    - grid_cells (List[Cell]): List of all grid cells in the maze.
    - sc (pygame.Surface): The screen surface for drawing the maze.

    Returns:
    - full_path (List[Cell]): The reconstructed path from the start to the destination once the 
      searches meet (if no path is found, return None).
    """
    
    # Define the start and destination cells
    start_cell = grid_cells[0]
    destination_cell = grid_cells[-1]

    # Two sets, two queues and two paent dicts to track the search from the start and the end and path visualization
    start_queue = []
    end_queue = []
    start_visited = set()
    end_visited = set()
    start_parent = {}
    end_parent = {}

    # Counter to track number of visited cells
    visited_cells_count = 0

    # Initialize queues and visited sets for both ends
    start_queue.append(start_cell)
    start_visited.add(start_cell)
    start_parent[start_cell] = None

    end_queue.append(destination_cell)
    end_visited.add(destination_cell)
    end_parent[destination_cell] = None

    # Main Bidirectional Search loop
    while start_queue and end_queue:

        # Process BFS from start side
        if start_queue:
            current_start_cell = start_queue.pop(0)
            current_start_cell.visited = True
            visited_cells_count += 1

            # Delay for visualization purposes
            pygame.time.delay(40)
            pygame.display.flip()

            # Redraw the entire maze
            for cell in grid_cells:
                cell.draw(sc)
            current_start_cell.draw(sc)

            # Check neighbors and continue exploring
            neighbors_start = current_start_cell.check_neighbors_for_search(grid_cells)
            for neighbor in neighbors_start:
                if neighbor not in start_visited:
                    start_queue.append(neighbor)
                    start_visited.add(neighbor)
                    start_parent[neighbor] = current_start_cell

                # Check if the search meets the end side
                if neighbor in end_visited:
                    full_path = reconstruct_bidirectional_path(sc, start_parent, end_parent, neighbor, start_cell, destination_cell)
                    return full_path, visited_cells_count

        # Process BFS from the end side and continue exploring
        if end_queue:
            current_end_cell = end_queue.pop(0)
            current_end_cell.visited = True
            visited_cells_count += 1

            # Delay for visualization purposes
            pygame.time.delay(60)
            pygame.display.flip()

            # Redraw the entire maze
            for cell in grid_cells:
                cell.draw(sc)
            current_end_cell.draw(sc)

            # Check neighbors
            neighbors_end = current_end_cell.check_neighbors_for_search(grid_cells)
            for neighbor in neighbors_end:
                if neighbor not in end_visited:
                    end_queue.append(neighbor)
                    end_visited.add(neighbor)
                    end_parent[neighbor] = current_end_cell

                # Check if the search meets the start side
                if neighbor in start_visited:
                    full_path = reconstruct_bidirectional_path(sc, start_parent, end_parent, neighbor, start_cell, destination_cell)
                    return full_path, visited_cells_count
        
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
    
    return None, visited_cells_count