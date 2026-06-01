import sys
import pygame
import numpy as np
from pygame.locals import *
pygame.init()
grid = []

# 0 = empty 1 = head, 2 = tail, 

def create_grid(size: int) -> None: # First time using type hints
    global grid
    print("Making a grid!")
    grid = []
    rows = []

    while len(rows) != size:
        rows.append(0)
    print(f"Made a row: {rows}")

    while len(grid) != size:
        grid.append(rows)
    print(f"Grid made: {grid}")


def find_thing(target: Any) -> tuple[int, int]:
    for row_idx, sublist in enumerate(grid):
        if target in sublist:
            col_idx = sublist.index(target)
            print(f"Found {target} at Row {row_idx}, Column {col_idx}")
            return (row_idx, col_idx)
    
    # Only runs if target is not found
    print(f"There's no {target} in this grid!")
    return (-1, -1) # Just a sentinel  value

def change_grid(place: tuple[int, int], value: Any):
    row, col = place
    grid[row][col] = value


class Player:
    def __init__(self,  score, player):
        self.score = score
        self.player = player

    def move_snake(direction: str):
        position = find_thing(1) # Is a tuple like (1, 5)

        if direction == "up": # Wooo spam!
            movement = (-1, 0)
        elif direction == "right":
            movement = (0, 1)
        elif direction == "down":
            movement = (1, 0)
        elif direction == "left":
            movement = (0, -1)
        else:
            movement = (0, 0)
            return
        
        change_grid(position, 2)
        position = (position[0] + movement[0], position[1] + movement[1]) # Tuple maths
        change_grid(position, 1)


while True:
    # Inputs bc im too lazy to put it in a class
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Because pkill is too hard
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or pygame.K_w:
                pass
            elif event.key == pygame.