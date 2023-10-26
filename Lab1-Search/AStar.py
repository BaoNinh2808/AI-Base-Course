from math import sqrt
from utils import *

def heuristic(State, Goal):
    #Euclide Distance
    return sqrt((Goal[0] - State[0])*(Goal[0] - State[0]) + (Goal[1] - State[1])*(Goal[1] - State[1]))

def estimate(State, Goal, curDis):
    return curDis + heuristic(State, Goal)

def findMinEstimate(open, goal, estimate):
    state, dis = open[0]
    minEstimate = estimate(state, goal, dis)
    index = 0
    for i in range(1, len(open)):
        state, dis = open[i]
        e = estimate(state, goal, dis)
        if e <= minEstimate:
            minEstimate = e
            index = i
    return index

def findAppearancePosition(State, set):
    for i in range(len(set)):
        if set[i][0] == State:
            return i
    return -1

def AStar(matrix, start, goal):
    open = [[start,0]]  #open set
    predessor = {}      #store the predessor of one cell - use for trace back

    while (len(open) > 0):  #is not empty 
        minEstimateIndex = findMinEstimate(open, goal, estimate)
        curState, curDis = open.pop(minEstimateIndex)

        #check if exit
        if (checkCompleted(curState, goal)):
            break

        #find neighbour cells that agent can move from the current cell (top, left, bottom, right)
        neighbours = findLegalCells(matrix, curState)
        
        #for each cell, check if is accessed yet - if not accessed yet, put it into the open list
        for cell in neighbours:
            o_index = findAppearancePosition(cell, open)
            if (tuple(cell) not in predessor) or (o_index >= 0 and open[o_index][1] > curDis+1):    #Convert to tuple for using dictionary
                open.append([cell, curDis+1])
                predessor[tuple(cell)] = curState   #set the predessor of this cell is curState
            
    if tuple(goal) not in predessor:    #Cann't find the path
        return None

    #find the path to exit 
    # Trace the path by backtracking from goal to start
    path = [goal]
    while path[len(path) - 1] != start:
        path.append(predessor[tuple(path[len(path) - 1])])

    return list(reversed(path))

def visualize_AStar_video(matrix, start, goal, bonus_points):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((720, 580))
    clock = pygame.time.Clock()
    running = True
    pause = False

    matrix[goal[0]][goal[1]] = 'G'
    for x,y,reward in bonus_points:
        matrix[x][y] = 'p'

    open = [[start,0]]  #open set
    predessor = {}      #store the predessor of one cell - use for trace back

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


        ##one step of Astar
        if (len(open) <= 0): break

        minEstimateIndex = findMinEstimate(open, goal, estimate)
        curState, curDis = open.pop(minEstimateIndex)

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
        
        if ((curState[0] != start[0]) or (curState[1] != start[1])):
                matrix[curState[0]][curState[1]] = 'o'
        #find neighbour cells that agent can move from the current cell (top, left, bottom, right)
        neighbours = findLegalCells(matrix, curState)
        
        #for each cell, check if is accessed yet - if not accessed yet, put it into the open list
        for cell in neighbours:
            o_index = findAppearancePosition(cell, open)
            if (tuple(cell) not in predessor) or (o_index >= 0 and open[o_index][1] > curDis+1):    #Convert to tuple for using dictionary
                open.append([cell, curDis+1])
                predessor[tuple(cell)] = curState   #set the predessor of this cell is curState
        
        ##Draw to screen
        screen.fill((255, 255, 255))  # Clear the screen
        draw_grid(screen, matrix, 700, 500)  # Draw the grid
        pygame.display.update()
        clock.tick(15)  # Limit the frame rate
