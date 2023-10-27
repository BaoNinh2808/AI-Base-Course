from heuristic import *
from utils import *
import queue

# Greedy Best-First Search (GBFS) algorithm implementation
def gbfs(matrix, bonus_points, start, goal, estimateFunction):
    open_cells = queue.PriorityQueue()  # Priority queue for open cells based on heuristic value
    open_cells.put((0, start))          # format (heuristic_value, cell) -> priority queue will sort in heuristic_value

    predecessor = {}    # Store the predecessor of each cell for tracing the path
    visit_list = []     # List to keep track of visited cells in order -> use for draw image after

    # While the open cells set is not empty
    while not open_cells.empty():  
        _, curState = open_cells.get()  # Get the cell with the lowest heuristic value
        visit_list.append(curState)     # Add this cell to the visited list

        # Check if we have reached the goal
        if checkComplete(curState, goal):
            break

        # Find neighboring cells that the agent can move to (top, left, bottom, right)
        neighbours = findLegalMoves(matrix, curState)

        # For each neighbor, check if it has not been accessed yet - if not, add it to the open_cells set
        for cell in neighbours:
            if cell not in predecessor:
                heuristic_value = estimateFunction(cell, goal)
                open_cells.put((heuristic_value, cell))
                predecessor[cell] = curState  # Set the predecessor of this cell as curState

    if goal not in predecessor:  # If no path to the goal is found
        return ([], visit_list)

    # Find the path to the exit by backtracking from the goal to the start
    path = [goal]
    while path[len(path)-1] != start:
        path.append(predecessor[path[len(path)-1]])

    return (list(reversed(path)), visit_list)

