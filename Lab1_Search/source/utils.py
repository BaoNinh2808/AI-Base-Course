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
    
    start = (0,0)
    goal = (0,0)
    # Iterate through all the matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (matrix[i][j] == 'S'):
                start = (i,j)
            if ((i == 0 and matrix[0][j] == ' ') or (j == 0 and matrix[i][0] == ' ')):
                goal = (i,j)
    
    return bonus_points, matrix, start, goal

def findLegalMoves(matrix, curState):
    # Get neighboring state
    neighbors = []

    x = curState[0]
    y = curState[1]

    if (matrix[x][y-1] != 'x'): #left
        neighbors.append((x,y-1))

    if (matrix[x][y+1] != 'x'): #right
        neighbors.append((x, y+1))

    if (matrix[x-1][y] != 'x'): #top
        neighbors.append((x-1, y))

    if (matrix[x+1][y] != 'x'): #bot
        neighbors.append((x+1, y))
    return neighbors

def checkComplete(current_cell, goal):
    if (current_cell[0] == goal[0] and current_cell[1] == goal[1]):
        return True
    return False

import pygame
import matplotlib.pyplot as plt
import vidmaker

def visualize_video(matrix, bonus_points, start, goal, WIDTH = 500, HEIGHT = 700, visit_list = None, path = None, outPath = "visualization_video.mp4"):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = 0
    
    video = vidmaker.Video(outPath, late_export=True)

    cell_size = min(WIDTH // len(matrix[0]), (HEIGHT-200) // len(matrix))
    screen.fill((255, 255, 255))  # Clear the screen

    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']
    for wall in walls:
        rect = pygame.Rect(wall[1] * cell_size, wall[0] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 0, 0), rect)  #black

    for x,y,reward in bonus_points:
        rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 255, 0), rect)  #Green

    rect_start = pygame.Rect(start[1] * cell_size, start[0] * cell_size, cell_size, cell_size)
    rect_goal   = pygame.Rect(goal[1] * cell_size, goal[0] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, (0, 0, 255), rect_start) #blue
    pygame.draw.rect(screen, (255, 0, 0), rect_goal) #red

    video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)

    #Stimulate the way that algorithm run
    for i in range(len(visit_list)):
        current_cell = visit_list[i]
        if (current_cell != start):
            rect = pygame.Rect(current_cell[1] * cell_size, current_cell[0] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 127, 0), rect)  #Orange
            video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)
            pygame.display.update()
            pygame.time.Clock().tick(15)

    #Draw finding path from start -> goal
    if path:
        for i in range(1, len(path)):
            current_cell = path[i]
            previous_cell = path[i-1]
            rect = pygame.Rect(current_cell[1] * cell_size, current_cell[0] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (128, 0, 128), rect)  #purple
            if (i == len(path)-1): # goal
                pygame.draw.rect(screen, (255, 0, 0), rect) #red

            point1 = pygame.Vector2(previous_cell[1] * cell_size + cell_size // 2, previous_cell[0] * cell_size + cell_size // 2)
            point2 = pygame.Vector2(current_cell[1] * cell_size + cell_size // 2, current_cell[0] * cell_size + cell_size // 2)
            pygame.draw.line(screen, (255, 255, 255), point1, point2) #white

            video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)
            pygame.display.update()
            pygame.time.Clock().tick(30)

    # Pause for look
    while (running < 10):
        running += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 10

        video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)
        pygame.display.update()
        clock.tick(15)

    video.export(verbose=True)

def visualize_maze(matrix, bonus, start, end, route=None, save_path=None):
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

    if save_path:
        # Save the plot as an image at the specified path (e.g., 'maze_visualization.png')
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1)
        
    plt.show()

    