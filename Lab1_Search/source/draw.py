import pygame
import matplotlib.pyplot as plt

def visualize_video(matrix, bonus_points, start, goal, WIDTH = 500, HEIGHT = 700, visit_list = None, path = None):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    pause = False

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

    #Stimulate the way that algorithm run
    for i in range(len(visit_list)):
        current_cell = visit_list[i]
        if (current_cell != start):
            rect = pygame.Rect(current_cell[1] * cell_size, current_cell[0] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 127, 0), rect)  #Orange
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

            pygame.display.update()
            pygame.time.Clock().tick(30)

    # Pause for look
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(15)

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