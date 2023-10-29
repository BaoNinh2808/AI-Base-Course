import pygame
import matplotlib.pyplot as plt
import vidmaker

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
            if ((i == 0 and matrix[0][j] == ' ') or (j == 0 and matrix[i][0] == ' ') or (i == len(matrix)-1 and matrix[i][j] == ' ') or (j == len(matrix[0])-1 and matrix[i][j] == ' ')):
                goal = (i,j)
    print(len(matrix[0]), len(matrix))
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

def visualize_video(matrix, bonus_points, start, goal, WIDTH = 720, HEIGHT = 540, visit_list = None, path = None, outPath = "visualization_video.mp4", title = "Search Algorithm"):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = 0
    
    padding = 50

    video = vidmaker.Video(outPath, late_export=True)

    cell_size = WIDTH // len(matrix[0])
    screen.fill((255, 255, 255))  # Clear the screen

    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']
    for wall in walls:
        rect = pygame.Rect(wall[1] * cell_size, padding + wall[0] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 0, 0), rect)  #black

    for x,y,reward in bonus_points:
        rect = pygame.Rect(y * cell_size, padding + x * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (0, 255, 0), rect)  #Green

    rect_start = pygame.Rect(start[1] * cell_size, padding + start[0] * cell_size, cell_size, cell_size)
    rect_goal   = pygame.Rect(goal[1] * cell_size, padding + goal[0] * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, (0, 0, 255), rect_start) #blue
    pygame.draw.rect(screen, (255, 0, 0), rect_goal) #red

    # Draw the menu
    menu_font = pygame.font.Font(None, 36)  # You can adjust the font and size
    menu_text = menu_font.render(title, True, (0, 0, 0))  # Render the text
    menu_rect = menu_text.get_rect()
    menu_rect.center = (WIDTH // 2, 15)  # Adjust the position of the menu

    # Draw the menu on the screen
    screen.blit(menu_text, menu_rect)

   # Dictionary to map color descriptions to color values and note text
    color_notes = {
        (0, 0, 255): "Start",
        (255, 0, 0): "Goal",
        (0, 255, 0): "Bonus Point",
        (255, 127, 0): "Visited",
        (128, 0, 128): "Route",
        # Add more color descriptions as needed
    }

    # Divide the color notes into two columns
    column1 = {}
    column2 = {}

    # Separate color notes into two columns
    for i, (color, description) in enumerate(color_notes.items()):
        if i % 2 == 0:
            column1[color] = (description)
        else:
            column2[color] = (description)

    # Draw the color notes for the first column
    note_font = pygame.font.Font(None, 20)  # You can adjust the font and size
    for i, (color, description) in enumerate(column1.items()):
        # Draw the color rectangle
        rect = pygame.Rect(10, HEIGHT - 100 + i * 30, 20, 20)
        pygame.draw.rect(screen, color, rect)
        
        # Render and draw the note text
        note_text = note_font.render(f"{description}", True, (0, 0, 0))  # Render the text
        note_rect = note_text.get_rect()
        note_rect.topleft = (40, HEIGHT - 100 + i * 30)
        screen.blit(note_text, note_rect)

    # Draw the color notes for the second column
    for i, (color, description) in enumerate(column2.items()):
        # Draw the color rectangle
        rect = pygame.Rect(250, HEIGHT - 100 + i * 30, 20, 20)
        pygame.draw.rect(screen, color, rect)
        
        # Render and draw the note text
        note_text = note_font.render(f"{description}", True, (0, 0, 0))  # Render the text
        note_rect = note_text.get_rect()
        note_rect.topleft = (280, HEIGHT - 100 + i * 30)
        screen.blit(note_text, note_rect)


    video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)

    #Stimulate the way that algorithm run
    for i in range(len(visit_list)):
        current_cell = visit_list[i]
        if (current_cell != start):
            rect = pygame.Rect(current_cell[1] * cell_size, padding + current_cell[0] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 127, 0), rect)  #Orange
            video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)
            pygame.display.update()
            pygame.time.Clock().tick(15)

    #Draw finding path from start -> goal
    if path:
        for i in range(1, len(path)):
            current_cell = path[i]
            previous_cell = path[i-1]
            rect = pygame.Rect(current_cell[1] * cell_size, padding + current_cell[0] * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (128, 0, 128), rect)  #purple
            if (i == len(path)-1): # goal
                pygame.draw.rect(screen, (255, 0, 0), rect) #red

            point1 = pygame.Vector2(previous_cell[1] * cell_size + cell_size // 2, padding + previous_cell[0] * cell_size + cell_size // 2)
            point2 = pygame.Vector2(current_cell[1] * cell_size + cell_size // 2, padding + current_cell[0] * cell_size + cell_size // 2)
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
    ax=plt.figure(figsize= (15,8), dpi=100).add_subplot(111)

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