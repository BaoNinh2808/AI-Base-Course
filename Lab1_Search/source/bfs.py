from utils import*

def bfs(matrix, start, goal):
    start = tuple(start)
    goal = tuple(goal)
    queue = [start]
    predessor = {}
    visit_list = []

    while queue:
        curState = queue.pop(0)
        
        if curState in visit_list:
            continue

        visit_list.append(curState)

        if checkComplete(curState, goal):
            break

        neighbours = findLegalMoves(matrix, curState)

        for cell in neighbours:
            cell_tuple = tuple(cell)
            if cell_tuple not in visit_list:
                queue.append(cell_tuple)
                predessor[cell_tuple] = curState

    if goal not in predessor:
        return None, visit_list

    path = [goal]
    while path[-1] != start:
        path.append(predessor[path[-1]])

    return list(reversed(path)), visit_list