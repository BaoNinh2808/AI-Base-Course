import os
import matplotlib.pyplot as plt
import pygame

def visualize_maze(matrix, bonus, start, end, route=None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v') #^
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^') #v
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    #2. Drawing the map
    ax=plt.figure(dpi=100).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=100,color='black')

    plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                marker='P',s=100,color='green')

    plt.scatter(start[1],-start[0],marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='silver')

    plt.text(end[1],-end[0],'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')

    for _, point in enumerate(bonus):
      print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

def read_file(file_name: str = 'maze.txt'):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))

  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()

  return bonus_points, matrix

def find_exit_position(matrix):

    # Iterate through the top and bottom edges
    for i in range(len(matrix)):
        if matrix[i][0] == ' ':
            return (i, 0)
        if matrix[i][-1] == ' ':
            return (i, len(matrix[0]) - 1)

    # Iterate through the left and right edges
    for j in range(len(matrix[0])):
        if matrix[0][j] == ' ':
            return (0, j)
        if matrix[-1][j] == ' ':
            return (len(matrix) - 1, j)

    return (0,0)

def find_start_position(matrix):

    # Iterate through all the matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (matrix[i][j] == 'S'):
                return (i,j) 
    return (0,0)

def checkCompleted(curState, Goal):
    if (curState[0] == Goal[0] and curState[1] == Goal[1]):
        return True
    return False

def findLegalCells(matrix, curState):
    # Get neighboring state
    neighbors = []

    x = curState[0]
    y = curState[1]

    if (matrix[x][y-1] != 'x'): #left
        neighbors.append([x,y-1])

    if (matrix[x][y+1] != 'x'): #right
        neighbors.append([x, y+1])

    if (matrix[x-1][y] != 'x'): #top
        neighbors.append([x-1, y])

    if (matrix[x+1][y] != 'x'): #bot
        neighbors.append([x+1, y])
    return neighbors

def draw_grid(screen, matrix, WIDTH, HEIGHT, path = None):
    cell_size = min(WIDTH // len(matrix[0]), HEIGHT // len(matrix))
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if cell == 'S':  # Start
                pygame.draw.rect(screen, (0, 0, 255), rect) #blue
            elif cell == 'G':  # Goal
                pygame.draw.rect(screen, (255, 0, 0), rect) #red
            elif cell == 'x':  # Wall
                pygame.draw.rect(screen, (0, 0, 0), rect)  #black
            elif cell == 'p':  # Point
                pygame.draw.rect(screen, (0, 255, 0), rect)  #Green
            elif cell == 'o': # Opened cell
                pygame.draw.rect(screen, (255, 127, 0), rect)  #Orange
            else:   #empty cell
                pygame.draw.rect(screen, (255, 255, 255), rect)  #White

    if path is not None:
        for i in range(1, len(path)-1):
            y, x = path[i]
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (128, 0, 128), rect) #purple

        for i in range(1, len(path)):
            y1, x1 = path[i-1]
            y2, x2 = path[i]
            point1 = pygame.Vector2(x1 * cell_size + cell_size // 2, y1 * cell_size + cell_size // 2)
            point2 = pygame.Vector2(x2 * cell_size + cell_size // 2, y2 * cell_size + cell_size // 2)
            pygame.draw.line(screen, (255, 255, 255), point1, point2) #white