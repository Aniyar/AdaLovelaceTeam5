import numpy as np
import copy
import pygame as pg
from tqdm import trange


class Grid:
    def __init__(self, a, b):
        self.width = a
        self.height = b
        self.grid = np.zeros((a, b), dtype=int)

    def infect(self, x, y):
        self.grid[x, y] = 1

    def update(self):
        neighbours = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        diagonals = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
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
        for i in range(1, self.width-1):
            for j in range(1, self.height-1):
                if (radius**2 >= (i - x)**2 + (j - y)**2):
                    self.grid[i, j] = 2


def generate_strategies(n):
    arr = []
    for i in range(n):
        strategy = {"x": np.random.randint(0, POLE_SIZE),
                    "y": np.random.randint(0, POLE_SIZE),
                    "r": np.random.randint(0, POLE_SIZE/5),
                    }
        arr.append(strategy)
    return arr


def evaluate(pole, strategy):
    simulation = copy.copy(pole)
    for i in range(26):
        simulation.update()
        if i % 5 == 0:
            simulation.throw(strategy["x"], strategy["y"], strategy["r"])
    # Evaluation: смотрим насколько хорошо справилась стратегия
    # для этого считаем сколько значений 0, 1, 2 осталось в гриде
    arr = simulation.grid.reshape(-1)
    k = 0
    k_1 = 0
    k_2 = 0
    for i in arr:
        if i == 1:
            k += 1
        if i == 2:
            k_1 += 1
        if i == 0:
            k_2 += 1
    strategy["infected"] = k
    strategy["pesticide"] = k_1
    strategy["grass"] = k_2
    return strategy


def breed(strategies):
    children = []
    for i in range(len(strategies)):
        for j in range(i, len(strategies)):
            p1 = strategies[i]
            p2 = strategies[j]
            child = {"x": (p1["x"]+p2["x"])/2, "y": (p1["y"]+p2["y"])/2, "r": (p1["r"]+p2["r"])/2}
            children.append(child)
    return children


POLE_SIZE = 100
pole = Grid(POLE_SIZE, POLE_SIZE)

infect_x, infect_y = np.random.randint(0, POLE_SIZE), np.random.randint(0, POLE_SIZE)
pole.infect(infect_x, infect_y)

first_gen = generate_strategies(50)
for i in trange((len(first_gen)), desc='Evaluating first Generation'):
    first_gen[i] = evaluate(pole, first_gen[i])

top = sorted(first_gen, key=lambda x: x["infected"], reverse=True)[:10]

# make children of best strategies and evaluate them for 3 generations 
generations = 3
for i in range(generations):
    top = sorted(top, key=lambda x: x["infected"], reverse=True)[:10]
    children = breed(top)
    for j in trange((len(children)), desc=f'Generation {i+2} Progress'):
        top.append(evaluate(pole, children[j]))

top = sorted(top, key=lambda x: x["infected"], reverse=True)[:5]
pg.init()


SCREEN_WIDTH = 600
screen = pg.display.set_mode((600, 600))
clock = pg.time.Clock()

colors = np.array([[120, 250, 90], [250, 90, 120], [255, 255, 255]])
surface = pg.surfarray.make_surface(colors[pole.grid])
surface = pg.transform.scale(surface, (600, 600))
running = True

m = 0
while running:
    m += 1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.blit(surface, (0, 0))
    pg.display.flip()

    clock.tick(60)
    pole.update()
    surface = pg.surfarray.make_surface(colors[pole.grid])
    surface = pg.transform.scale(surface, (SCREEN_WIDTH, SCREEN_WIDTH))
    if m % 5 == 0:
        pole.throw(top[0]["x"], top[0]["y"], top[0]["r"])
        pole.throw(top[1]["x"], top[1]["y"], top[1]["r"])
        pole.throw(top[2]["x"], top[2]["y"], top[2]["r"])
        pole.throw(top[3]["x"], top[3]["y"], top[3]["r"])
        pole.throw(top[4]["x"], top[4]["y"], top[4]["r"])
    
    if m % 25 == 0:
        pole = Grid(100, 100)
        pole.infect(infect_x, infect_y)



# pip install tqdm