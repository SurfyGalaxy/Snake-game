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
        grid.append(rows.copy())
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
    if row < 0 or col < 0 or row >= len(grid) or col >=  len(grid):
        print(f"Invalid position {place}")
        return
    grid[row][col] = value


class Player:
    def __init__(self,  score, player):
        self.score = score
        self.player = player

        if player == "WASD":
            self.movement = (0, 1)   # Moving right
        else:
            self.movement = (0, -1)  # Moving left

    def process_input(self, direction: str):
        

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
        self.movement = movement
    
    def move_snake(self):
        id_offset = 0
        if self.player == "Arrows":
            id_offset = 10
        position = find_thing(1 + id_offset) # Is a tuple like (1, 5)

        change_grid(position, 2 + id_offset)
        position = (position[0] + self.movement[0], position[1] + self.movement[1]) # Tuple maths
        change_grid(position, 1 + id_offset)


# Pygame time!
# Expect extremely messy code, code which doesn't make sense and no semblence of PEP compliance


size = width, height = 320, 240 # Screen size
screen = pygame.display.set_mode(size) # Idk man this is just what we have ti di
while True:
    # Inputs bc im too lazy to put it in a class
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Because pkill is too hard
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if event.key == pygame.K_UP:
                    print("P1 Up")
                elif event.key == pygame.K_w:
                    print("P2 up")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if event.key == pygame.K_RIGHT:
                    print("P1 Right")
                elif event.key == pygame.K_d:
                    print("P2 Right")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if event.key == pygame.K_DOWN:
                    print("P1 Down")
                elif event.key == pygame.K_s:
                    print("P2 Down")
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if event.key == pygame.K_LEFT:
                    print("P1 Left")
                elif event.key == pygame.K_a:
                    print("P2 Left")
    
    screen.fill("purple")
    pygame.display.flip()