from heuristic import *
from utils import *

def findAppearancePosition(open_list, current_cell):
    for i in range(len(open_list)):
        if (current_cell == open_list[0]):
            return i
    return -1


def AStar(matrix, bonus_points, start, goal, estimateFunction):
    open_list = [[start,0]]  #open set
    predessor = {}      #store the predessor of one cell - use for trace back
    visit_list = []

    while (len(open_list) > 0):  #is not empty 
        index = findCandicateElement(open_list, goal, estimateFunction)
        curState, curDis = open_list.pop(index)
        visit_list.append(curState)

        #check if exit
        if (checkComplete(curState, goal)):
            break

        #find neighbour cells that agent can move from the current cell (top, left, bottom, right)
        neighbours = findLegalMoves(matrix, curState)
        
        #for each cell, check if is accessed yet - if not accessed yet, put it into the open list
        for cell in neighbours:
            o_index = findAppearancePosition(cell, open_list)
            if (tuple(cell) not in predessor) or (o_index >= 0 and open_list[o_index][1] > curDis+1):    #Convert to tuple for using dictionary
                open_list.append([cell, curDis+1])
                predessor[tuple(cell)] = curState   #set the predessor of this cell is curState
            
    if tuple(goal) not in predessor:    #Cann't find the path
        return None, visit_list

    #find the path to exit 
    # Trace the path by backtracking from goal to start
    path = [goal]
    while path[len(path) - 1] != start:
        path.append(predessor[tuple(path[len(path) - 1])])

    return list(reversed(path)), visit_list