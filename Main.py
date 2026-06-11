import sys
import pygame
import numpy as np
from pygame.locals import *
pygame.init()
grid = []

# 0 = empty 1 = head, 2 = tail, 

def create_grid(size: int) -> None: # First time using type hints
    global grid
    grid = []
    rows = []

    while len(rows) != size:
        rows.append(0)

    while len(grid) != size:
        grid.append(rows.copy())


def find_thing(target: Any) -> tuple[int, int]:
    for row_idx, sublist in enumerate(grid):
        if target in sublist:
            col_idx = sublist.index(target)
            return (row_idx, col_idx)
    
    return (-1, 0) # Just a sentinel  value

def change_grid(place: tuple[int, int], value: Any):
    row, col = place
    if row < 0 or col < 0 or row >= len(grid) or col >=  len(grid):
        #print(f"Invalid position {place}")
        return
    print("Done")
    grid[row][col] = value

def render_grid(screen, grid, cell_size, offset_x, offset_y):
    """Apparently this is  a docstring
    pretty cool"""
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            # Calculate pixel position
            x = offset_x + (col_idx * cell_size)
            y = offset_y + (row_idx * cell_size)
            
            if cell == 0:  # Empty
                color = (40, 40, 40)  # Dark gray
            elif cell == 1:  # WASD Head
                color = (0, 255, 0)  # Bright green
            elif 2 <= cell <= 10:  # WASD Body
                intensity = 100 + (cell * 15)
                color = (0, intensity, 0)
            elif cell == 11:  # Arrow Head
                color = (255, 0, 0)  # Bright red
            elif 12 <= cell <= 20:  # Arrow Body
                intensity = 100 + ((cell - 10) * 15)
                color = (intensity, 0, 0)
            else:  
                color = (255, 255, 0)  
            
            
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            
            pygame.draw.rect(screen, (80, 80, 80), (x, y, cell_size, cell_size), 1)


class Player:
    def __init__(self,  size, player):
        self.size = size
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
        self.id_offset = 1000 if self.player == "Arrows" else 0
        
        head_pos = find_thing(self.size + self.id_offset)
        if head_pos == (-1, -1):
            return
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = grid[row][col]
                if self.id_offset < cell <=  self.id_offset + 100:
                    if cell - 1 == self.id_offset: 
                        change_grid((row, col), 0)  
                    else:
                        change_grid((row, col), cell - 1) 
        
        new_head = (head_pos[0] + self.movement[0], head_pos[1] + self.movement[1])
        change_grid(new_head, self.size + self.id_offset)
        
        
        

# And now for actual code which runs:
size = width, height = 320, 240 # Screen size
screen = pygame.display.set_mode(size) # Idk man this is just what we have ti do
GRID_SIZE = 16

create_grid(GRID_SIZE)
change_grid((4, 4), 10)
change_grid((4, 8), 110)
p1 = Player(size=10, player="Arrows")
p2 = Player(size=10, player="WASD")

cell_pixel_size = 15 
grid_offset_x = (320 - (GRID_SIZE * cell_pixel_size)) // 2
grid_offset_y = (240 - (GRID_SIZE * cell_pixel_size)) // 2

clock = pygame.time.Clock()
frame = 0


# Pygame time!
# Expect extremely messy code, code which doesn't make sense and no semblence of PEP compliance


while True: 
    # Inputs bc im too lazy to put it in a class
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Because pkill is too hard
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if event.key == pygame.K_UP:
                    p1.process_input("up")
                elif event.key == pygame.K_w:
                    p2.process_input("up")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if event.key == pygame.K_RIGHT:
                    p1.process_input("right")
                elif event.key == pygame.K_d:
                    p2.process_input("right")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if event.key == pygame.K_DOWN:
                    p1.process_input("down")
                elif event.key == pygame.K_s:
                    p2.process_input("down")
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if event.key == pygame.K_LEFT:
                    p1.process_input("left")
                elif event.key == pygame.K_a:
                    p2.process_input("left")

    if frame == 12:
        p1.move_snake()
        p2.move_snake()
        frame = 0


    screen.fill("purple")

    render_grid(screen, grid, cell_pixel_size, grid_offset_x, grid_offset_y)
    
    pygame.display.flip()
    clock.tick(60)
    frame += 1