from math import sqrt
from utils import *

def heuristic(State, Goal): 
    #Euclide Distance
    return sqrt((Goal[0] - State[0])*(Goal[0] - State[0]) + (Goal[1] - State[1])*(Goal[1] - State[1]))

def findMinHeuristic(open, goal, heuristic):
    minHeuristic = heuristic(open[0], goal)
    index = 0
    for i in range(1, len(open)):
        h = heuristic(open[i], goal)
        if h <= minHeuristic:
            minHeuristic = h
            index = i
    return index

def gbfs(matrix, start, goal):
    open = [start]  #open set
    predessor = {}  #store the predessor of one cell - use for trace back

    while (len(open) > 0):  #is not empty 
        minHeuristicIndex = findMinHeuristic(open, goal, heuristic)
        curState = open.pop(minHeuristicIndex)

        #check if exit
        if (checkCompleted(curState, goal)):
            break

        #find neighbour cells that agent can move from the current cell (top, left, bottom, right)
        neighbours = findLegalCells(matrix, curState)
        
        #for each cell, check if is accessed yet - if not accessed yet, put it into the open list
        for cell in neighbours:
            if tuple(cell) not in predessor:    #Convert to tuple for using dictionary
                open.append(cell)
                predessor[tuple(cell)] = curState   #set the predessor of this cell is curState

    if tuple(goal) not in predessor:    #Cann't find the path
        return None

    #find the path to exit 
    # Trace the path by backtracking from goal to start
    path = [goal]
    while path[len(path) - 1] != start:
        path.append(predessor[tuple(path[len(path) - 1])])

    return list(reversed(path))


def visualize_gfbs_video(matrix, start, goal, bonus_points):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((720, 580))
    clock = pygame.time.Clock()
    running = True
    pause = False

    matrix[goal[0]][goal[1]] = 'G'
    for x,y,reward in bonus_points:
        matrix[x][y] = 'p'

    open = [start]  #open set
    predessor = {}  #store the predessor of one cell - use for trace back

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()
            clock.tick(1) 


        ##one step of GFBS
        if (len(open) <= 0): break

        minHeuristicIndex = findMinHeuristic(open, goal, heuristic)
        curState = open.pop(minHeuristicIndex)

        #check if exit
        if (curState[0] == goal[0] and curState[1] == goal[1]):
            pause = True
            if tuple(goal) not in predessor:    #Cann't find the path
                continue

            #find the path to exit 
            # Trace the path by backtracking from goal to start
            path = [goal]
            while path[len(path) - 1] != start:
                path.append(predessor[tuple(path[len(path) - 1])])

            ##Draw to screen
            screen.fill((255, 255, 255))  # Clear the screen
            draw_grid(screen, matrix, 700, 500, path)  # Draw the grid
            pygame.display.update()
            clock.tick(15)  # Limit the frame rate
            continue
        
        if (curState[0] != start[0] or curState[1] != start[1]):
            matrix[curState[0]][curState[1]] = 'o'
        #find neighbour cells that agent can move from the current cell (top, left, bottom, right)
        neighbours = findLegalCells(matrix, curState)
        
        #for each cell, check if is accessed yet - if not accessed yet, put it into the open list
        for cell in neighbours:
            if tuple(cell) not in predessor:    #Convert to tuple for using dictionary
                open.append(cell)
                predessor[tuple(cell)] = curState   #set the predessor of this cell is curState
        
        ##Draw to screen
        screen.fill((255, 255, 255))  # Clear the screen
        draw_grid(screen, matrix, 700, 500)  # Draw the grid
        pygame.display.update()
        clock.tick(15)  # Limit the frame rate


