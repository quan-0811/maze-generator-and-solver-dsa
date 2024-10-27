import pygame
from config import *

pygame.init()
sc = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()

class Cell:
    """
    Represents a single cell in the maze with coordinates, walls, and states for maze generation and solving.

    Attributes:
    - x (int): The x-coordinate of the cell in the grid.
    - y (int): The y-coordinate of the cell in the grid.
    - walls (dict): A dictionary indicating whether each wall ('top', 'right', 'bottom', 'left') exists (True)
      or has been removed (False).
    - generated (bool): Indicates if the cell has been visited during maze generation.
    - visited (bool): Indicates if the cell has been visited during the search/solving process.
    - is_solution (bool): Marks if the cell is part of the final solution path.
    """

    def __init__(self, x, y):
        """
        Initializes a Cell with specific x, y coordinates and sets up its walls and other states.

        Args:
        - x (int): The x-coordinate of the cell in the maze grid.
        - y (int): The y-coordinate of the cell in the maze grid.
        """

        # Grid cells position
        self.x, self.y = x, y
        self.walls = {"top": True,
                      "right": True,
                      "bottom": True,
                      "left": True}
        
        # Flags
        self.generated = False
        self.visited = False
        self.is_solution = False

    def draw_current_cell(self):
        """
        Highlights the current cell by drawing a rectangle on the screen with a distinct color.
        """

        # Calculate the position of the cell in the display based on grid coordinates
        x, y = self.x * TILE_SIZE + MAZE_OFFSET, self.y * TILE_SIZE + 2
        pygame.draw.rect(sc, pygame.Color(START_END_CELL_COLOR), (x, y, TILE_SIZE - 2, TILE_SIZE - 2))

    def draw(self, sc: pygame.Surface):
        """
        Draws the cell on the screen based on its current state, including walls and whether 
        it's generated, visited, or part of the solution.

        Args:
        - sc (pygame.Surface): The Pygame surface on which the cell is drawn.
        """

        # Calculate the position of the cell in the display based on grid coordinates
        x, y = self.x * TILE_SIZE + MAZE_OFFSET, self.y * TILE_SIZE + 2

        # Draw different colors depending on the state of the cell (generated, visited, part of the solution).
        if self.generated and not self.visited:
            pygame.draw.rect(sc, CELL_GENERATED_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
        if self.generated and self.visited and not self.is_solution:
            pygame.draw.rect(sc, CELL_VISITED_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
        if self.generated and self.visited and self.is_solution:
            pygame.draw.rect(sc, CELL_SOLUTION_COLOR, (x, y, TILE_SIZE, TILE_SIZE))

        # Drawing the walls of the cell (top, right, bottom, left) if they exist.
        if self.walls['top']:
            pygame.draw.line(sc, WALL_COLOR, (x, y), (x + TILE_SIZE, y), 5)
        if self.walls['right']:
            pygame.draw.line(sc, WALL_COLOR, (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), 5)
        if self.walls['bottom']:
            pygame.draw.line(sc, WALL_COLOR, (x + TILE_SIZE, y + TILE_SIZE), (x , y + TILE_SIZE), 5)
        if self.walls['left']:
            pygame.draw.line(sc, WALL_COLOR, (x, y + TILE_SIZE), (x, y), 5)
    
    def check_cell(self, grid_cells, x, y):
        """
        Checks if a cell exists at the given (x, y) coordinates and returns the cell if valid.
        
        Args:
        - grid_cells (List[Cell]): List of all cells in the maze grid.
        - x (int): The x-coordinate of the cell to check.
        - y (int): The y-coordinate of the cell to check.
        
        Returns:
        - Cell or False: The cell at the given coordinates if valid, otherwise False.
        """

        # Lambda function to calculate the index of the cell in the 1D list of grid cells.
        find_index = lambda x, y: x + y * cols

        # If the coordinates are outside the valid grid range, return False.
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        
        # Return the cell at the specified coordinates.
        return grid_cells[find_index(x, y)]
    
    def check_neighbors_for_maze_gen(self, grid_cells):
        """
        Finds and returns a list of unvisited neighboring cells for maze generation.
        
        Args:
        - grid_cells (List[Cell]): List of all cells in the maze grid.
        
        Returns:
        - neighbors (List[Cell]): A list of neighboring cells that have not yet been generated.
        
        Neighbors are identified by checking adjacent cells (top, right, bottom, left).
        If no unvisited neighbors are found, it returns False.
        """

        neighbors = []

        # Check each direction (top, right, bottom, left) for valid neighbors.
        top = self.check_cell(grid_cells, self.x, self.y - 1)
        right = self.check_cell(grid_cells, self.x + 1, self.y)
        bottom = self.check_cell(grid_cells, self.x, self.y + 1)
        left = self.check_cell(grid_cells, self.x - 1, self.y)

        # Append neighbors that haven't been generated yet (unvisited).
        if top and not top.generated:
            neighbors.append(top)
        if right and not right.generated:
            neighbors.append(right)
        if bottom and not bottom.generated:
            neighbors.append(bottom)
        if left and not left.generated:
            neighbors.append(left)

        # Return the list of available neighbors or False if no neighbors found.
        if len(neighbors) > 0:
            return neighbors
        else:
            return False 
    
    def check_neighbors_for_search(self, grid_cells):
        """
        Finds and returns a list of unvisited neighboring cells for maze-solving.

        Args:
        - grid_cells (List[Cell]): List of all cells in the maze grid.

        Returns:
        - neighbors: A list of unvisited neighboring cells that can be explored in the maze-solving process.
        
        This method checks for neighbors that have no walls separating them from the current cell, ensuring that they are reachable.
        """

        neighbors = []

        # Check each direction (top, right, bottom, left) for valid neighbors and make sure walls are open.
        top = self.check_cell(grid_cells, self.x, self.y - 1)
        right = self.check_cell(grid_cells, self.x + 1, self.y)
        bottom = self.check_cell(grid_cells, self.x, self.y + 1)
        left = self.check_cell(grid_cells, self.x - 1, self.y)

        # Append neighbors where walls are open and the neighbor is not visited.
        if top and not top.visited:
            if self.walls["top"] == False and top.walls["bottom"] == False:
                neighbors.append(top)
        if right and not right.visited:
            if self.walls["right"] == False and right.walls["left"] == False:
                neighbors.append(right)
        if bottom and not bottom.visited:
            if self.walls["bottom"] == False and bottom.walls["top"] == False:
                neighbors.append(bottom)
        if left and not left.visited:
            if self.walls["left"] == False and left.walls["right"] == False:
                neighbors.append(left)

        # Return the list of available neighbors.
        if len(neighbors) > 0:
            return neighbors
        else:
            return []