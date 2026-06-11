import sys
import pygame
import numpy as np
from typing import Any
from pygame.locals import *
pygame.init()
grid = []

target_fps = 8 # (starting) fps
speedup_interval = 20 # How quickly to speedup by 1fps 
speedup_amount = 1 # How much to increase fps
offset = 1000 # Im sure this'll never have to be edited... right?
""" Because i'm too good for writing this anywhere else

1-999 = P1
1,000 - 1999 = P2
0 = Empty
-1 = Food """

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
    
    return (-1, -1) # Just a sentinel  value

def see_thing(place):
    thing = grid[place[0]][place[1]] # 1 liner goes brrrr
    return thing

def change_grid(place: tuple[int, int], value: Any):
    row, col = place
    if row < 0 or col < 0 or row >= len(grid) or col >=  len(grid):
        #print(f"Invalid position {place}")
        return
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
            elif cell == 10:  # WASD Head
                color = (0, 255, 0)  # Bright green
            elif 2 <= cell <= 110:  # WASD Body
                intensity = 100 + ((cell % 10) * 15)  # Cycles every 10 segments
                color = (0, intensity, 0)
            elif cell == 10 + offset:  # Arrow Head
                color = (255, 0, 0)  # Bright red
            elif 2 + offset <= cell <= 110 + offset:  # Arrow Body
                intensity = 100 + (((cell - offset) % 10) * 15)  # Cycles every 10 segments
                color = (intensity, 0, 0)
            else:  
                color = (255, 255, 0)  # Food
            
            
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))
            
            pygame.draw.rect(screen, (80, 80, 80), (x, y, cell_size, cell_size), 1)


def player_dead(dead, location):
    if dead == "WASD":
        if see_thing(location) == p2_size + offset: # ey P2's also here
            winner = "Draw"
        else:
            winner = "Arrows"
    else:
        if see_thing(location) == p1_size: # eyyy P1's here
            winner = "Draw"
        else:
            winner = "WASD"
    if winner == "Draw":
        print("Wow. Nobody won. How about you two don't hit eachother's heads for once?")
    else:
        print(f"Oh wow player using {dead} lost, good job {winner}")
    pygame.quit() # temporary until i add rounds
    sys.exit()

class Player:
    def __init__(self, player):
        self.player = player

        if player == "WASD":
            self.size = p1_size
            self.movement = (0, 1)   # Moving right at start
        else:
            self.size = p2_size
            self.movement = (0, -1)  # Moving left at start
            

    def process_input(self, direction: str):
        
        if direction == "up" and self.movement != (1, 0): # Wooo spam!
            movement = (-1, 0)
        elif direction == "right" and self.movement != (0, -1):
            movement = (0, 1)
        elif direction == "down" and self.movement != (-1, 0):
            movement = (1, 0)
        elif direction == "left" and self.movement != (0, -1):
            movement = (0, -1)
        else:
            movement = self.movement
        self.movement = movement
    
    def move_snake(self):
        if self.player == "Arrows":
            self.id_offset = offset
        else:
            self.id_offset = 0
        
        head_pos = find_thing(self.size + self.id_offset)
        if head_pos == (-1, -1):
            player_dead(self.player, self.old_head)
            return
        
        new_head = (head_pos[0] + self.movement[0], head_pos[1] + self.movement[1])
        
        if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or 
            new_head[1] < 0 or new_head[1] >= GRID_SIZE):
            player_dead(self.player, self.old_head)
            return
        
        no = see_thing(new_head)
        
        if no > 0:
            player_dead(self.player, self.old_head)
            return
        
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = grid[row][col]
                if self.id_offset < cell <= self.id_offset + 100:
                    if cell - 1 == self.id_offset: 
                        change_grid((row, col), 0)  
                    else:
                        change_grid((row, col), cell - 1)
        
        # Handle something
        if no == -1:
            self.size += 1
        
        self.old_head = new_head
        change_grid(new_head, self.size + self.id_offset)
    
        

        
        

# And now for actual code which runs:
size = width, height = 640, 480 # Screen size
screen = pygame.display.set_mode(size) # Idk man this is just what we have ti do
GRID_SIZE = 16

create_grid(GRID_SIZE)
change_grid((4, 4), 10)
change_grid((8, 8), 1010)
change_grid((10, 2), -1)
change = speedup_amount
p1_size = 10
p2_size = 10
p1 = Player(player="Arrows")
p2 = Player(player="WASD")

cell_pixel_size = 30 
grid_offset_x = (640 - (GRID_SIZE * cell_pixel_size)) // 2
grid_offset_y = (480 - (GRID_SIZE * cell_pixel_size)) // 2
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

    if str(frame / target_fps).endswith(".0"): # bc 12 is 60 (native fps) / 5 (target fps)
        p1.move_snake()
        p2.move_snake()
    

    screen.fill("purple")

    render_grid(screen, grid, cell_pixel_size, grid_offset_x, grid_offset_y)
    
    pygame.display.flip()
    clock.tick(60)
    frame += 1