import numpy as np

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
        


pole = Grid(40, 40)
pole.infect(23, 29)
print("Infected grid")
pole.print_grid()
for i in range(2):
    pole.update()
print("\nUpdated grid")
pole.print_grid()