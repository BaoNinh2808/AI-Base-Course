from search_algorithm.heuristic import *
from search_algorithm.utils import *
from search_algorithm.point_heuristic import *
import math

def pickup_point_heuristic(matrix, bonus_points, start, goal, estimateFunction):
    visit_list = []  # List to keep track of visited cells in order -> use for draw image after
    route = []
    travelled_points = []

    arrange_points = []
    for x,y,reward in bonus_points:
        point_est = estimateFunction((x,y), goal)
        arrange_points.append((point_est, (x,y)))

    arrange_points.sort(key=lambda point: point[0])
    far_point = arrange_points[-1]

    current_start = start
    # While not attempt to goal
    while (not checkComplete(current_start, goal)):
        travelled_points.append(current_start)

        new_goal = goal
        for _,point in arrange_points:
            if point not in travelled_points:
                new_goal = point
                break

        new_route, new_visit_list, new_start = astart_modify(matrix, bonus_points, travelled_points, current_start, new_goal, goal, estimateFunction)
        
        #update variables
        visit_list.extend(new_visit_list)
        route.extend(new_route)
        current_start = new_start

        # Cann't finding any legal path
        if (not new_route):
            return ([], visit_list)
        
    return (route, visit_list)