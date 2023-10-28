from search_algorithm.heuristic import *
from search_algorithm.utils import *

import queue

# A* algorithm implementation
def astar(matrix, bonus_points, start, goal, estimateFunction):
    open_cells = [(0, start)]  # Open cells set with initial cell (0, start) - format (estimate_value, cell)

    predecessor = {}  # Store the predecessor of each cell for tracing the path
    visit_list = []  # List to keep track of visited cells in order -> use for draw image after

    # While there are open cells to explore
    while open_cells:
        open_cells.sort(key=lambda cell: cell[0])  # Sort the open cells by estimate cost
        estDis, curState = open_cells.pop(0)  # Get the cell with the lowest estimate cost
        visit_list.append(curState)  # Add this cell to the visited list

        # Check if we have reached the goal
        if checkComplete(curState, goal):
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

    if goal not in predecessor:  # If no path to the goal is found
        return ([], visit_list)

    # Find the path to the exit by backtracking from the goal to the start
    path = [goal]
    while path[len(path)-1] != start:
        path.append(predecessor[path[len(path)-1]])

    return (list(reversed(path)), visit_list)
