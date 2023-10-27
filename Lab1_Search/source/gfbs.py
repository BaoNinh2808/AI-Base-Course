from heuristic import*
from utils import*

def gbfs(matrix, bonus_points, start, goal, estimateFunction):
    open = [start]  #open set
    predessor = {}  #store the predessor of one cell - use for trace back
    visit_list = []

    while (len(open) > 0):  #is not empty 
        index = findCandicateElement(open, goal, estimateFunction)
        curState = open.pop(index)
        visit_list.append(curState)

        #check if exit
        if (checkComplete(curState, goal)):
            break

        #find neighbour cells that agent can move from the current cell (top, left, bottom, right)
        neighbours = findLegalMoves(matrix, curState)
        
        #for each cell, check if is accessed yet - if not accessed yet, put it into the open list
        for cell in neighbours:
            if tuple(cell) not in predessor:    #Convert to tuple for using dictionary
                open.append(cell)
                predessor[tuple(cell)] = curState   #set the predessor of this cell is curState

    if tuple(goal) not in predessor:    #Cann't find the path
        return None, visit_list

    #find the path to exit 
    # Trace the path by backtracking from goal to start
    path = [goal]
    while path[len(path) - 1] != start:
        path.append(predessor[tuple(path[len(path) - 1])])

    return list(reversed(path)), visit_list