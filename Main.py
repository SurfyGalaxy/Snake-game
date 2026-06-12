import sys
import pygame
import numpy as np
import random
import pygame_widgets
from typing import Any
from pygame.locals import *
from pygame_widgets.button import Button
pygame.init()
grid = []

# Soon to be a YAML File :)
target_fps = 5# (starting) fps
speedup_interval = 20 # How quickly to speedup by 1fps (in seconds)
speedup_amount = 0.2 # percentage to increase speed by
offset = 1000 # Im sure this'll never have to be edited... right?
grid_size = 32 # How big should the grid be?
padding = 100 # How many pixels off the sides should the grid be?
fruits = 2 # How many fruit s to spawn?
start_size = 10 # How long to start snakes?
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
    global mode
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
    mode = "not Game"

def spawn_food(count):
    while count != 0:
        place = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
        if see_thing(place) == 0:
            change_grid(place, -1)
        else:
            spawn_food(1)
        count -= 1

p1_size = start_size
p2_size = start_size

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
        elif direction == "left" and self.movement != (0, 1):
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
        
        if (new_head[0] < 0 or new_head[0] >= grid_size or 
            new_head[1] < 0 or new_head[1] >= grid_size):
            player_dead(self.player, self.old_head)
            return
        
        no = see_thing(new_head)
        
        if no > 0:
            player_dead(self.player, self.old_head)
            return
        
        for row in range(grid_size):
            for col in range(grid_size):
                cell = grid[row][col]
                if self.id_offset < cell <= self.id_offset + 100:
                    if cell - 1 == self.id_offset: 
                        change_grid((row, col), 0)  
                    else:
                        change_grid((row, col), cell - 1)
        
        # Handle something
        if no == -1:
            self.size += 1
            spawn_food(1)
        
        self.old_head = new_head
        change_grid(new_head, self.size + self.id_offset)
    
        
class game():
    def __init__(self):
        self.frame = 0
    
    def run_game(self):
        global grid, cell_pixel_size, grid_offset_x, grid_offset_y, target_fps, speedup_amount, speedup_interval, p1, p2
        if self.frame % (60 // target_fps) == 0:
            p1.move_snake()
            p2.move_snake()
        
        if self.frame % (60 * speedup_interval) == 0 and self.frame > 0:
            target_fps = int(target_fps * (1 + speedup_amount))
            if target_fps > 60:
                target_fps = 60

        screen.fill("black")

        render_grid(screen, grid, cell_pixel_size, grid_offset_x, grid_offset_y)
        self.frame += 1
    
    def main_menu(self):
        render_main_menu(screen)
        screen.fill("black")
        
def do_thing():
    global mode
    mode = "Game"
    init_game()
def init_first_game():
    global monitor_size, size, screen
    monitor_size = pygame.display.get_desktop_sizes()
    size = width, height = monitor_size[0][0], monitor_size[0][1] # Screen size
    screen = pygame.display.set_mode(size) # Idk man this is just what we have ti do
def init_game():
    # And now for actual code which runs:
    global monitor_size, size, screen, change, p1, p2, cell_pixel_size, grid_offset_x, grid_offset_y
    p1_size = start_size
    p2_size = start_size
    create_grid(grid_size)
    change_grid((grid_size // 4, grid_size // 2), 10)
    change_grid((grid_size - grid_size // 4, grid_size // 2), 1010)
    spawn_food(fruits)
    change = speedup_amount
    
    p1 = Player(player="Arrows")
    p2 = Player(player="WASD")
init_first_game()
init_game()
if monitor_size[0][0] <= monitor_size[0][1]: # For the psycos with vertical monitors
    cell_pixel_size = (monitor_size[0][0] - padding) // grid_size
else:
    cell_pixel_size = (monitor_size[0][1] - padding) // grid_size
grid_offset_x = (monitor_size[0][0] - (grid_size * cell_pixel_size)) // 2
grid_offset_y = (monitor_size[0][1] - (grid_size * cell_pixel_size)) // 2
clock = pygame.time.Clock()

button = Button(screen, monitor_size[0][0] // 2 - 150, monitor_size[0][1] // 2 - 72, 300, 150, text="Start!", onClick=lambda: do_thing())



# Pygame time!
# Expect extremely messy code, code which doesn't make sense and no semblence of PEP compliance
game = game()
mode = "not Game"
while True: 
    # Inputs bc im too lazy to put it in a class
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Because pkill is too hard
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and mode == "Game":
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

    if mode == "Game":
        game.run_game()
    elif mode == "not Game":
        screen.fill("black")
        pygame_widgets.update(event)
    
    
    pygame.display.flip()
    clock.tick(60)
    