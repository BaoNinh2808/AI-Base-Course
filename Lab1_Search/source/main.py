import os
from a_star import *
from gfbs import *
from heuristic import *
from draw import *
from utils import *


filePath = "level_1.txt"
bonus_points, matrix, start, goal = read_file(filePath)

print(f'The height of the matrix: {len(matrix)}')
print(f'The width of the matrix: {len(matrix[0])}')

#path = gbfs(matrix, start, goal)
#visualize_maze(matrix,bonus_points,start,goal,path)
#visualize_gfbs_video(matrix, start, goal, bonus_points)

path, visit_list = AStar(matrix, bonus_points, start, goal, heuristic_1)
visualize_maze(matrix,bonus_points,start,goal,path)
visualize_video(matrix=matrix, bonus_points=bonus_points, start=start, goal=goal, path=path, visit_list=visit_list)
