from search_algorithm.utils import *

# Breadth-First Search (BFS) algorithm implementation
"""
Using 2D matrix to manage visited cell, it will help to improve the performance than just finding the visited cell in the list
"""
def bfs(matrix, start, goal):
    queue = [start]     # Queue for BFS traversal
    predecessor = {}    # Store the predecessor of each cell for tracing the path
    visit_list = []     # List to keep track of visited cells in order -> use for draw image after
    
    # Use a 2D matrix to track if a cell has been visited
    visited = [[False for _ in range(len(matrix[0]))] for _ in range(len(matrix))]

    while queue:
        curState = queue.pop(0)

        # Skip cells that have already been visited
        if curState in visit_list:
            continue
        
        visited[curState[0]][curState[1]] = True    # Update this cell is visited
        visit_list.append(curState) # Add it to the visit_list as the continue visited cell

        # Check if we have reached the goal
        if checkComplete(curState, goal):
            break

        # Find neighboring cells that the agent can move to (top, left, bottom, right)
        neighbours = findLegalMoves(matrix, curState)

        for cell in neighbours:
            # If the neighbor has not been visited, add it to the queue
            if not visited[cell[0]][cell[1]]:
                queue.append(cell)
                predecessor[cell] = curState

    if goal not in predecessor:  # If no path to the goal is found
        return ([], visit_list)

    # Find the path to the exit by backtracking from the goal to the start
    path = [goal]
    while path[len(path)-1] != start:
        path.append(predecessor[path[len(path)-1]])

    return (list(reversed(path)), visit_list)
