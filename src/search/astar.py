import pygame
import heapq  # For priority queue functionality
from config import *
from typing import List
from cell import Cell
from utils import reconstruct_path, manhattan_distance, draw_text_of_running_alg, draw_button

def solve_maze_A_star(grid_cells: List[Cell], sc: pygame.Surface):
    """
    Solve the maze using the A* algorithm, which combines features of both Dijkstra's 
    algorithm and greedy best-first search. The function uses a priority queue to explore the 
    grid cells and applies the Manhattan distance heuristic to guide the search towards the 
    destination.

    Args:
    - grid_cells (List[Cell]): A list of all cells in the maze, each cell is an object with 
      properties such as neighbors, coordinates, and methods for search and drawing.
    - sc (pygame.Surface): The pygame screen surface used for drawing the maze and visualizing 
      the search process.

    Returns:
    - path (List{Cell}): A list of cells representing the solution path from the start to the 
      destination else None
    - visited_cells_count (int): The total number of cells visited during the search.
    """

    # Define the start and destination cells
    start_cell = grid_cells[0]
    destination_cell = grid_cells[-1]

    # Counter to track number of visited cells
    visited_cells_count = 0

    # Priority queue for the open set (stores cells to be evaluated) (holds tuples of (f_cost, id, cell))
    open_set = []
    heapq.heappush(open_set, (0, id(start_cell), start_cell))

    # G cost: actual distance from start to current cell
    g_cost = {cell: float('inf') for cell in grid_cells}
    # Initialize g_cost for all cells as infinity
    g_cost[start_cell] = 0  # G cost for the start cell is 0

    # F cost: G cost + heuristic (estimated distance to goal)
    f_cost = {cell: float('inf') for cell in grid_cells}
    # Initialize f_cost for all cells as infinity
    f_cost[start_cell] = manhattan_distance(start_cell, destination_cell)  
    # F cost for the start cell is the heuristic to the destination

    # Initialize visited set; parent dictionary for path reconstruction
    parent = {}
    parent[start_cell] = None
    visited = set()

    # Main loop for A* search
    while open_set:
        # Pop the cell with the lowest f_cost from the priority queue
        _, _, current_cell = heapq.heappop(open_set)
        # Mark the current cell as visited
        current_cell.visited = True
        visited_cells_count += 1

        # If we reached the destination, reconstruct the path
        if current_cell == destination_cell:
            path = reconstruct_path(sc, parent, start_cell, destination_cell)
            return path, visited_cells_count

        # Redraw the entire maze on each iteration to keep all cells visible
        for cell in grid_cells:
            cell.draw(sc)

        # Draw the visited cell
        current_cell.draw(sc)

        # Display the current state of the algorithm
        draw_text_of_running_alg(sc, "RUNNING: A Star", FONT, 17, 20, 230, "#FFFFFF")
        draw_text_of_running_alg(sc, "CELLS EXPLORED: " + str(visited_cells_count), FONT, 17, 20, 260, "#FFFFFF")

        # Draw buttons
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

        # Explore neighbors of the current cell
        neighbors = current_cell.check_neighbors_for_search(grid_cells)
        for neighbor in neighbors:
            # Skip visited cells
            if neighbor in visited:
                continue

            # Tentative g_cost (distance to neighbor through current)
            tentative_g_cost = g_cost[current_cell] + 1  # Distance between adjacent cells is 1
            # If a shorter path is found
            if tentative_g_cost < g_cost[neighbor]:
                # Set the current cell as the parent of the neighbor
                parent[neighbor] = current_cell
                # Update g_cost for the neighbor
                g_cost[neighbor] = tentative_g_cost
                # Update f_cost with the new g_cost and heuristic (Manhattan distance)
                f_cost[neighbor] = g_cost[neighbor] + manhattan_distance(neighbor, destination_cell)

                # Add the neighbor to the open_set if it's not already there
                if neighbor not in [item[2] for item in open_set]:
                    heapq.heappush(open_set, (f_cost[neighbor], id(neighbor), neighbor))
    
    return None, visited_cells_count
