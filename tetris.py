# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:40:01 2023

@author: simard
"""

import pygame
import random

pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Set the width and height of each grid location
WIDTH = 20
HEIGHT = 20
MARGIN = 5

# Set the grid size
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Set the screen size
SCREEN_WIDTH = (WIDTH + MARGIN) * GRID_WIDTH + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * GRID_HEIGHT + MARGIN

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the window title
pygame.display.set_caption("Tetris")

# Set up the grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Define the shapes
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 1], [1, 0, 0]]
]

# Define colors for the shapes
shape_colors = [RED, BLUE, GREEN, CYAN, ORANGE, PURPLE, YELLOW]

# Define the game clock
clock = pygame.time.Clock()

# Define the current piece
current_piece = []
current_piece_color = None
current_piece_x = GRID_WIDTH // 2 - 1
current_piece_y = 0

# Define the game over flag
game_over = False

# Define the score
score = 0

# Function to create a new piece
def new_piece():
    global current_piece, current_piece_color, current_piece_x, current_piece_y
    current_piece = random.choice(shapes)
    current_piece_color = random.choice(shape_colors)
    current_piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
    current_piece_y = 0
new_piece()
# Function to check if the piece can be placed at the current position
def valid_space():
    global current_piece_x, current_piece_y
    for y in range(len(current_piece)):
        for x in range(len(current_piece[0])):
            if current_piece[y][x] == 1:
                if (
                    x + current_piece_x < 0
                    or x + current_piece_x >= GRID_WIDTH
                    or y + current_piece_y >= GRID_HEIGHT
                    or grid[y + current_piece_y][x + current_piece_x] != 0
                ):
                    return False
    return True

# Function to lock the piece in place and check for completed rows
def lock_piece():
    global grid, current_piece, current_piece_x, current_piece_y, score
    for y in range(len(current_piece)):
        for x in range(len(current_piece[0])):
            if current_piece[y][x] == 1:
                grid[y + current_piece_y][x + current_piece_x] = current_piece_color
    for y in range(len(grid)):
        if all(grid[y]):
            for i in range(y, 1, -1):
                grid[i] = grid[i - 1].copy()
            grid[0] = [0] * GRID_WIDTH
            score += 10

# Function to draw the grid and the current piece
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = grid[y][x]
            pygame.draw.rect(
                screen,
                color,
                [
                    (MARGIN + WIDTH) * x + MARGIN,
                    (MARGIN + HEIGHT) * y + MARGIN,
                    WIDTH,
                    HEIGHT,
                ],
            )

    if current_piece is not None:
        for y in range(len(current_piece)):
            for x in range(len(current_piece[0])):
                if current_piece[y][x] == 1:
                    pygame.draw.rect(
                        screen,
                        current_piece_color,
                        [
                            (MARGIN + WIDTH) * (x + current_piece_x) + MARGIN,
                            (MARGIN + HEIGHT) * (y + current_piece_y) + MARGIN,
                            WIDTH,
                            HEIGHT,
                        ],
                    )

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT:
                current_piece_x -= 1
                if not valid_space():
                    current_piece_x += 1

            if event.key == pygame.K_RIGHT:
                current_piece_x += 1
                if not valid_space():
                    current_piece_x -= 1

            if event.key == pygame.K_DOWN:
                current_piece_y += 1
                if not valid_space():
                    current_piece_y -= 1

            if event.key == pygame.K_UP:
                current_piece = list(zip(*reversed(current_piece)))

    if not game_over:
        current_piece_y += 1
        if not valid_space():
            current_piece_y -= 1
            lock_piece()
            new_piece()
            if not valid_space():
                game_over = True

    screen.fill(BLACK)

    draw_grid()

    # Draw the score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))

    if game_over:
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, RED)
        screen.blit(
            text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2)
        )

    pygame.display.flip()

    clock.tick(10)

pygame.quit()
