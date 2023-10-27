
def findCandicateElement(open_list, goal, estimateFunction):
    minEstValue = estimateFunction(open_list[0][0], goal)
    index = 0
    for i in range(1, len(open_list)):
        estValue = estimateFunction(open_list[i][0], goal)
        if estValue <= minEstValue:
            minEstValue = estValue
            index = i
    return index

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