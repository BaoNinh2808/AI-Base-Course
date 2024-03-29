from search_algorithm.heuristic import *
from search_algorithm.utils import *
import math

# Point Heuristic algorithm implementation 
# Point Heuristic using for map have point to find the short path in proper time
def point_heuristic(matrix, bonus_points, start, goal, estimateFunction):
    visit_list = []  # List to keep track of visited cells in order -> use for draw image after
    route = []
    travelled_points = []

    point_earn = 0
    current_start = start
    # While not attempt to goal
    while (not checkComplete(current_start, goal)):
        travelled_points.append(current_start)

        #find candicate point
        isRight = 1
        if ((goal[1] - current_start[1]) < 0):
            isRight = -1
        isTop = 1
        if ((goal[0] - current_start[0]) < 0):
            isTop = -1

        points = []
        for x, y, reward in bonus_points:
            if ((x,y) in travelled_points): continue
            if (x - current_start[0]) * isTop < 0 or (y - current_start[1]) * isRight < 0:
                continue 
            points.append(((x,y), reward))

        est_val = estimateFunction(current_start, goal)
        candicate_points = []
        for i in range(len(points)):
            point, reward = points[i]
            point_est = estimateFunction(current_start, point) + estimateFunction(point, goal) + reward
            if (point_est < est_val):
                candicate_points.append((point_est, point, reward))

        candicate_points.sort(key=lambda point: point[0])  # Sort by estimate cost 
        
        new_goal = goal
        if candicate_points:
            distance = float('inf')
            for point_est, point, reward in candicate_points:
                new_distance = sqrt((current_start[0]-point[0])**2 + (current_start[1]-point[1])**2)
                if (new_distance < distance):
                    distance = new_distance
                    new_goal = point

        new_route, new_visit_list, new_start = astart_modify(matrix, bonus_points, travelled_points, current_start, new_goal, goal, estimateFunction) 
        #update variables
        visit_list.extend(new_visit_list)
        route.extend(new_route)
        current_start = new_start

        # Cann't finding any legal path
        if (not new_route):
            return ([], visit_list, point_earn)
        
        #update point earn in the way
        for x,y,reward in bonus_points: 
            if (x,y) == current_start:
                point_earn += reward 

    return (route, visit_list, point_earn)

def astart_modify(matrix, bonus_points, travelled_points, start, goal, realGoal, estimateFunction):
    open_cells = [(0, start)]  # Open cells set with initial cell (0, start) - format (estimate_value, cell)
    predecessor = {}  # Store the predecessor of each cell for tracing the path
    visit_list = []  # List to keep track of visited cells in order -> use for draw image after

    isRealGoal = False
    isMeetPoint = False
    curState = start
    # While there are open cells to explore
    while open_cells:
        open_cells.sort(key=lambda cell: cell[0])  # Sort the open cells by estimate cost
        estDis, curState = open_cells.pop(0)  # Get the cell with the lowest estimate cost
        visit_list.append(curState)  # Add this cell to the visited list

        for x,y,reward in bonus_points: #Accidently meet bonus point
            if (curState == (x,y) and curState not in travelled_points):
                isMeetPoint = True
                break
        if (isMeetPoint): break

        # Check if we have reached the goal point
        if checkComplete(curState, goal):
            break

        # Check if we have reached the real goal
        if checkComplete(curState, realGoal):
            isRealGoal = True
            break    
        curDis = estDis - estimateFunction(curState, goal)  # real current cost g(n) = f(n) - h(n)

        # Find neighboring cells that the agent can move to (top, left, bottom, right)
        neighbours = findLegalMoves(matrix, curState)

        # For each neighbor, check if it has not been accessed yet or has a lower estimate value than itseft in the open list
        for cell in neighbours:
            index = next((i for i, x in enumerate(open_cells) if x[1] == cell), -1) #find the index of cell in the open list - if no appearance, return -1
            estimate_value = curDis + 1 + estimateFunction(cell, goal)

            # If the cell has not been accessed or has a lower estimate, add it to the open cells
            if (cell not in predecessor) or (index >= 0 and estimate_value < open_cells[index][0]):
                open_cells.append((estimate_value, cell))
                predecessor[cell] = curState  # Set the predecessor of this cell as curState

    if (isMeetPoint == True):
        path = [curState]
        while path[len(path)-1] != start:
            path.append(predecessor[path[len(path)-1]])
        return (list(reversed(path)), visit_list, curState)
    
    if (isRealGoal == True):
        path = [realGoal]
        while path[len(path)-1] != start:
            path.append(predecessor[path[len(path)-1]])
        return (list(reversed(path)), visit_list, realGoal)
    
    if goal not in predecessor:  # If no path to the goal is found
        return ([], visit_list, goal)
    
    # Find the path to the exit by backtracking from the goal to the start
    path = [goal]
    while path[len(path)-1] != start:
        path.append(predecessor[path[len(path)-1]])

    return (list(reversed(path)), visit_list, goal)