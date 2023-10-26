from gbfs import*
from utils import *
from AStar import*

bonus_points, matrix = read_file('input1.txt')

print(f'The height of the matrix: {len(matrix)}')
print(f'The width of the matrix: {len(matrix[0])}')

start = find_start_position(matrix)
goal = find_exit_position(matrix)

#path = gbfs(matrix, start, goal)
#visualize_maze(matrix,bonus_points,start,goal,path)
#visualize_gfbs_video(matrix, start, goal, bonus_points)

path = AStar(matrix, start, goal)
visualize_maze(matrix,bonus_points,start,goal,path)
visualize_AStar_video(matrix, start, goal, bonus_points)