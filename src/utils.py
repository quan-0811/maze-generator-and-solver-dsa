import pygame
from random import choice
from config import *
from typing import List, Dict
from cell import Cell

def generate_maze(grid_cells: List[Cell], sc: pygame.Surface, current_cell: Cell, destination_cell: Cell, stack: list):
    """
    Generate the maze using recursive backtracking algorithm.
    
    Args:
    - grid_cells (List[Cell]): List of all grid cells.
    - sc (pygame.Surface): The screen surface (pygame object).
    - current_cell (Cell): The current cell being processed.
    - destination_cell (Cell): The final destination cell in the maze.
    - stack (List[Cell]): Stack of visited cells.

    Returns:
    - current_cell (Cell): Updated current cell.
    - stack (List[Cell]): Updated stack of visited cells.
    - maze_complete (bool): Boolean flag indicating whether the maze generation is complete.
    """
    
    # Draw each cell in the grid
    for cell in grid_cells:
        cell.draw(sc)
    
    # Mark the current cell as generated and draw it
    current_cell.generated = True
    current_cell.draw_current_cell()
    destination_cell.draw_current_cell()
    
    # Visualize the stack (the path that is being carved out)
    for i, cell in enumerate(stack):
        pygame.draw.rect(sc, CELL_GENERATED_COLOR, (cell.x * TILE_SIZE + MAZE_OFFSET + 3, cell.y * TILE_SIZE + 4, TILE_SIZE - 4, TILE_SIZE - 4))

    # Check for available neighbors to continue generating the maze
    neighbors = current_cell.check_neighbors_for_maze_gen(grid_cells)
    
    if neighbors:
        # Randomly select a neighbor to continue the maze path and mark it as generated
        next_cell = choice(neighbors)
        next_cell.generated = True
        # Push current cell to the stack for backtracking
        stack.append(current_cell)
        # Remove the wall between the current and next cells and move to the next cell
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        # If no cells are left, the maze is complete
        current_cell = stack.pop()
    else:
        # Return the final state
        maze_complete = True
        return current_cell, stack, maze_complete
    
    return current_cell, stack, False

def reset_maze(grid_cells: List[Cell]):
    """
    Resets the maze to its initial state by resetting the cells' walls and states.
    
    Args:
    - grid_cells (List[Cell]): List of all grid cells.

    Returns:
    - stack: Empty stack used for maze generation.
    - maze_complete: Boolean flag indicating the maze generation is not complete.
    - maze_generating: Boolean flag indicating maze generation is in progress.
    """
    # Reset all cells to their initial state
    for cell in grid_cells:
        cell.generated = False
        cell.visited = False
        cell.is_solution = False
        cell.walls = {"top": True, "right": True, "bottom": True, "left": True}

    # Reset the data structures and flags
    stack = []
    maze_complete = False
    maze_generating = True
    
    return stack, maze_complete, maze_generating

def draw_maze(grid_cells: List[Cell], sc: pygame.Surface, stack: list, current_cell: Cell, destination_cell: Cell):
    """
    Draw the current state of the maze including cells, the current cell, 
    and the stack representing the carved path.

    Args:
    - grid_cells (List[Cell]): List of all cells in the maze.
    - sc (pygame.Surface): The pygame surface for drawing the maze.
    - stack (List[Cell]): The stack representing the current carved path in the maze.
    - current_cell (Cell): The current cell being processed.
    - destination_cell (Cell): The destination cell (goal) in the maze.
    """

    # Draw each cell in the grid
    for cell in grid_cells:
        cell.draw(sc)  

    # Draw the current cell and the destination cell
    current_cell.draw_current_cell()
    destination_cell.draw_current_cell()
    
    # Visualize the path (stack) as it gets carved through the maze
    for i, cell in enumerate(stack):
        pygame.draw.rect(sc, CELL_GENERATED_COLOR, (cell.x * TILE_SIZE + MAZE_OFFSET + 3, cell.y * TILE_SIZE + 4, TILE_SIZE - 4, TILE_SIZE - 4), border_radius = 4)

def reset_cells_visited_state(grid_cells: List[Cell]):
    """
    Reset the visited and solution state for all cells in the grid.

    Args:
    - grid_cells (List[Cell]): List of all cells in the maze grid.
    """
    
    # Reset the visited and solution state for each cell
    for cell in grid_cells:
        cell.visited = False
        cell.is_solution = False

def remove_walls(current: Cell, next: Cell):
    """
    Remove walls between the current cell and the next cell to create a path.
    
    Args:
    - current (Cell): The current cell being processed.
    - next (Cell): The next cell that is adjacent to the current cell.
    """

    # Calculate the difference in x-coordinates and y-coordinates
    dx = current.x - next.x
    dy = current.y - next.y

    # If the next cell is to the left of the current cell
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False

    # If the next cell is to the right
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    
    # If the next cell is above
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False

    # If the next cell is below
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def reconstruct_path(sc: pygame.Surface, parent: Dict[Cell, Cell], start_cell: Cell, destination_cell: Cell):
    """
    Reconstruct the path from the start cell to the destination cell using the parent dictionary.

    This function backtracks from the destination cell to the start cell using the `parent` dictionary, 
    which stores the predecessor of each cell. It marks the cells along the path as part of the solution 
    and updates the visual representation of the maze in pygame as the path is being reconstructed.

    Args:
    - sc (pygame.Surface): The pygame screen surface used to visualize the path.
    - parent (Dict[Cell, Cell]): A dictionary where the keys are cells, and values are the parent cells from which 
      they were reached. Used to backtrack and find the solution path.
    - start_cell (Cell): The initial cell in the maze.
    - destination_cell (Cell): The target cell in the maze.

    Returns:
    - path (List[Cell]): A list of cells representing the solution path from start to destination.
    """

    # Initialize an empty list to store the path
    path = []
    # Start the backtracking from the destination cell
    current_cell = destination_cell

    # Backtrack from destination to start using the parent dictionary
    while current_cell is not None:
        # Mark the cell as part of the solution path
        current_cell.is_solution = True
        # Add the current cell to the path list
        path.append(current_cell)
        # Redraw the cell
        current_cell.draw(sc)
        pygame.display.flip()
        # Move to the previous cell
        current_cell = parent[current_cell]
    
    # Reverse the path since we built it from the destination to start
    path.reverse()
    return path

def reconstruct_bidirectional_path(sc: pygame.Surface, start_parent: Dict[Cell, Cell], end_parent: Dict[Cell, Cell], meeting_cell: Cell, start_cell: Cell, destination_cell: Cell):
    """
    Reconstruct the path once the bidirectional search has found a common cell.
    Combines the path from the start to the meeting cell and the meeting cell to the destination.

    Args:
    - sc (pygame.Surface): The screen surface for drawing the maze.
    - start_parent (Dict[Cell, Cell]): Parent dictionary from the start search.
    - end_parent (Dict[Cell, Cell]): Parent dictionary from the end search.
    - meeting_cell (Cell): The cell where the two searches meet.
    - start_cell (Cell): The starting cell.
    - destination_cell (Cell): The destination cell.

    Returns:
    - full_path (List[Cell]): The full path from the start to the destination through the meeting point.
    """

    # Mark the meeting cell as part of the solution
    meeting_cell.is_solution = True
    meeting_cell.visited = True
    meeting_cell.draw(sc)
    pygame.display.flip()

    # Reconstruct the path from the start to the meeting point
    path_start = []
    current_cell = meeting_cell
    while current_cell is not None:
        current_cell.is_solution = True
        path_start.append(current_cell)
        current_cell.draw(sc)
        pygame.display.flip()
        current_cell = start_parent[current_cell]

    # Reconstruct the path from the meeting point to the destination
    path_end = []
    current_cell = end_parent[meeting_cell]
    while current_cell is not None:
        current_cell.is_solution = True
        path_end.append(current_cell)
        current_cell.draw(sc)
        pygame.display.flip()
        current_cell = end_parent[current_cell]

    # Full path from start to meeting + meeting to destination
    full_path = path_start[::-1] + path_end
    return full_path

def manhattan_distance(cell1: Cell, cell2: Cell):
    """
    Heuristic function to calculate the Manhattan distance between two cells.

    The Manhattan distance is the sum of the absolute differences between the x and y 
    coordinates of the two cells. This heuristic is commonly used in grid-based pathfinding 
    algorithms like A*.

    Args:
    - cell1 (Cell): The first cell (starting cell).
    - cell2 (Cell): The second cell (destination cell).

    Returns:
    - int: The Manhattan distance between the two cells.
    """
    return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

def draw_button(sc: pygame.Surface, text:str, x_offset: int, y_offset: int, color):
    """
    Draw a button with text on the screen.

    Args:
    - sc (pygame.Surface): The screen surface where the button will be drawn.
    - text (str): The label text to be displayed on the button.
    - x_offset (int): The x-coordinate offset for positioning the button.
    - y_offset (int): The y-coordinate offset for positioning the button.
    - color (tuple/str): RGB tuple representing the color of the button background.

    Returns:
    - pygame.Rect: The rectangle object representing the button for event handling.
    """

    # Define the button font and size
    btn_font = pygame.font.SysFont(FONT, size = 19, bold = True)
    # Render the text to be displayed on the button
    btn_surf = btn_font.render(text, True, "#FFFFFF")
    # Create a button rectangle with the given position and size
    btn = pygame.Rect(x_offset, y_offset, 200, 40)

    # Draw the button with rounded corners
    pygame.draw.rect(sc, color, btn, border_radius = 5)  

    # Blit the text surface onto the screen, centered on the button
    sc.blit(btn_surf, (btn.x + (btn.width - btn_surf.get_width()) // 2, btn.y + (btn.height - btn_surf.get_height()) // 2))

    return btn

def draw_text_of_running_alg(sc: pygame.Surface, text:str, font: str, size: int, x_offset: int, y_offset: int, color):
    """
    Write the info of the running search algorithm on the screen.

    Args:
    - sc (pygame.Surface): The screen surface where the text will be drawn.
    - text (str): The label text to be displayed on the text.
    - x_offset (int): The x-coordinate offset for positioning the text.
    - y_offset (int): The y-coordinate offset for positioning the text.
    - color (tuple): RGB tuple representing the color of the text.
    """

    text_area = pygame.Rect(x_offset, y_offset, 200, 30)  # Adjust width and height if needed
    # Clear the text area by filling it with the background color (e.g., black)
    sc.fill(BACKGROUND_COLOR, text_area)

    # Set up font and render the text
    font = pygame.font.SysFont(font, size = size, bold = True)
    text_obj = font.render(text, True, color)
    # Set top-left as the position
    text_rect = text_obj.get_rect(topleft = (x_offset, y_offset))
    # Draw the text on the screen
    sc.blit(text_obj, text_rect)

