import pygame
from cell import Cell
from config import *
from search.bfs import solve_maze_BFS
from search.dfs import solve_maze_DFS
from search.bidirectionalbfs import solve_maze_bidirectional_BFS
from search.astar import solve_maze_A_star
from search.gbfs import solve_maze_greedy_bfs
from utils import reset_cells_visited_state, draw_button, draw_maze, generate_maze, reset_maze, draw_text_of_running_alg

# Initialize Pygame
pygame.init()
sc = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()  

# Load logo image
image = pygame.image.load("images\logo.png")
image = pygame.transform.scale(image, (240, 240))

# Create a grid of Cell objects, define the starting cell, destination cell and flags
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
destination_cell = grid_cells[-1]
stack = []
maze_generating = False
maze_complete = False
searching_completed = False
running_txt = ""
cells_cnt = 0

# Main game loop
while True:
    sc.fill(pygame.Color(BACKGROUND_COLOR))

    # Display the logo
    sc.blit(image, (3, 0))

    # Check for user events
    for event in pygame.event.get():
        # If the user clicks the window close button, exit.
        if event.type == pygame.QUIT:
            exit()
        # Check if the mouse was clicked.
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click.
            mouse_pos = pygame.mouse.get_pos()

            # Only respond to mouse clicks if the maze isn't being generated.
            if not maze_generating:

                # Check which button was clicked.
                if maze_gen_btn.collidepoint(mouse_pos):
                    stack, maze_complete, maze_generating = reset_maze(grid_cells)
                    searching_completed = False

                elif bfs_btn.collidepoint(mouse_pos):
                    running_txt = "RUNNING: BFS"
                    searching_completed = False
                    reset_cells_visited_state(grid_cells)
                    searching_completed = True
                    _, cells_cnt = solve_maze_BFS(grid_cells, sc)

                elif dfs_btn.collidepoint(mouse_pos):
                    running_txt = "RUNNING: DFS"
                    searching_completed = False
                    reset_cells_visited_state(grid_cells)
                    _, cells_cnt = solve_maze_DFS(grid_cells, sc)
                    searching_completed = True

                elif bidirectional_btn.collidepoint(mouse_pos):
                    running_txt = "RUNNING: Bidirectional BFS"
                    searching_completed = False
                    reset_cells_visited_state(grid_cells)
                    _, cells_cnt = solve_maze_bidirectional_BFS(grid_cells, sc)
                    searching_completed = True

                elif astar_btn.collidepoint(mouse_pos):
                    running_txt = "RUNNING: A Star"
                    searching_completed = False
                    reset_cells_visited_state(grid_cells)
                    _, cells_cnt = solve_maze_A_star(grid_cells, sc)
                    searching_completed = True

                elif gbfs_btn.collidepoint(mouse_pos):
                    running_txt = "RUNNING: GBFS"
                    searching_completed = False
                    reset_cells_visited_state(grid_cells)
                    _, cells_cnt = solve_maze_greedy_bfs(grid_cells, sc)
                    searching_completed = True
    
    # Draw the buttons for generating the maze and running different algorithms.
    maze_gen_btn = draw_button(sc, "GENERATE MAZE", 20, 300, BUTTON_COLOR)
    bfs_btn = draw_button(sc, "BFS", 20, 400, BUTTON_COLOR)
    dfs_btn = draw_button(sc, "DFS", 20, 350, BUTTON_COLOR)
    bidirectional_btn = draw_button(sc, "BIDIRECTIONAL BFS", 20, 450, BUTTON_COLOR)
    astar_btn = draw_button(sc, "A STAR", 20, 500, BUTTON_COLOR)
    gbfs_btn = draw_button(sc, "GBFS", 20, 550, BUTTON_COLOR)

    # Draw the maze grid with cells, stack (for maze generation), and the start and destination cells.
    draw_maze(grid_cells, sc, stack, current_cell, destination_cell)

    # If maze generation is active and not yet complete, continue generating the maze.
    if maze_generating and not maze_complete:
        draw_text_of_running_alg(sc, "GENERATING MAZE", FONT, 17, 45, 230, "#FFFFFF")
        current_cell, stack, maze_complete = generate_maze(grid_cells, sc, current_cell, destination_cell, stack)

    # If maze generation is complete, stop generation
    if maze_complete:
        maze_generating = False

    # Display the result of the search algorithm
    if searching_completed and not maze_generating:
        draw_text_of_running_alg(sc, running_txt, FONT, 17, 20, 230, "#FFFFFF")
        draw_text_of_running_alg(sc, "CELLS EXPLORED: " + str(cells_cnt), FONT, 17, 20, 260, "#FFFFFF")
    
    # Update the display and set the frame rate.
    pygame.display.flip()
    clock.tick(500)
    
    
