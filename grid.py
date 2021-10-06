import numpy as np
import pygame
import random 
import math
import pygame as pg


class Grid():
    def __init__(self, a, b):
        self.width = a
        self.height = b
        self.grid = np.zeros((a, b), dtype=int)
    
    def infect(self, x, y):
        self.grid[x, y] = 1

    def update(self):
        neighbours = [(1, 0), (0,1), (-1,0), (0,-1)]
        diagonals = [(1,1), (-1,1), (-1,-1), (1,-1)]
        updated = self.grid.copy()
        for i in range(1, self.width-1):
            for j in range(1, self.height-1):
                if self.grid[i, j] == 1:
                    for n in neighbours:
                        updated[i+n[0], j+n[1]] = 1
                    for d in diagonals:
                        if np.random.rand() > 0.2:
                            updated[i+d[0], j+d[1]] = 1
        self.grid = updated
        


    
    def print_grid(self):
        for i in range(self.width):
            for j in range(self.height):
                print(self.grid[i, j], end=" ")
            print("\n", end="")

    def throw(self, x, y, radius):
        # допустим x = 5, y =4, radius =2 
        # тогда [5, 4], [5, 5], [5, 6], [5, 4], [5, 3]
        # (x-x0)^2 + (y - y0)^2 <= R^2      
        for i in range(1, self.width-1):
            for j in range(1, self.height-1):                
                if (radius**2 >= (i - x)**2 + (j - y)**2):
                    self.grid[i, j] = 2



colors = np.array([[120, 250, 90], [250, 90, 120], [255, 255, 255]])

POLE_SIZE = 1000
pole = Grid(POLE_SIZE, POLE_SIZE)
pole.infect(np.random.randint(0, POLE_SIZE), np.random.randint(0, POLE_SIZE))

pg.init()

SCREEN_WIDTH = 600
screen = pg.display.set_mode((600, 600))
clock = pg.time.Clock()

colors = np.array([[120, 250, 90], [250, 90, 120], [255, 255, 255]])
surface = pg.surfarray.make_surface(colors[pole.grid])
surface = pg.transform.scale(surface, (SCREEN_WIDTH, SCREEN_WIDTH))  # Scaled a bit.
running = True

m = 0 
while running:
    m += 1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((30, 30, 30))
    screen.blit(surface, (100, 100))
    pg.display.flip()

    clock.tick(60)
    pole.update()
    surface = pg.surfarray.make_surface(colors[pole.grid])
    surface = pg.transform.scale(surface, (SCREEN_WIDTH, SCREEN_WIDTH)) 
    if m % 5 == 0:
        pole.throw(np.random.randint(0, POLE_SIZE), np.random.randint(0, POLE_SIZE), np.random.randint(0, 100))






