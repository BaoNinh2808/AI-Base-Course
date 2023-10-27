from utils import *
import queue

# Uniform Cost Search (UCS) algorithm implementation
def ucs(matrix, start, goal):
    predecessor = {}    # Store the predecessor of each cell for tracing the path
    visit_list = []     # List to keep track of visited cells in order -> use for draw image after

    open_cells = queue.PriorityQueue()  # Priority queue for open cells based on cost
    open_cells.put((0, start))          # Format is (cost, state) -> the priority queue will arrange by the first argument (cost)

    cost_so_far = {}  # Store visited nodes with their cost - using dictionary for search and replace efficient
    cost_so_far[start] = 0

    while not open_cells.empty():
        curCost, curState = open_cells.get()  # Get the cell with the least cost
        visit_list.append(curState) # Add it to the visit_list as the continue visited cell

        if checkComplete(curState, goal):
            break
        
        
        # Find neighboring cells that the agent can move to (top, left, bottom, right)
        neighbours = findLegalMoves(matrix, curState)

        for cell in neighbours:
            newCost = curCost + 1  # Assuming uniform cost of 1 for all moves

            #if not access this cell before or it is accessed with the higher cost than now -> add to open list
            if (cell not in cost_so_far) or (newCost < cost_so_far[cell]):
                cost_so_far[cell] = newCost
                open_cells.put((newCost, cell))
                predecessor[cell] = curState

    if goal not in predecessor:  # If no path to the goal is found
        return ([], visit_list)

    # Find the path to the exit by backtracking from the goal to the start
    path = [goal]
    while path[len(path)-1] != start:
        path.append(predecessor[path[len(path)-1]])

    return (list(reversed(path)), visit_list)

