from math import sqrt

"""Manhattan Distance
"""
#Sum of absolute values of differences in the goal’s x and y coordinates and the current cell’s x and y coordinates respectively,
#Often use when the agent just move top, left, bottom or right

def heuristic_1(current_cell, goal):
    return abs(current_cell[0] - goal[0]) + abs (current_cell[1] - goal[1])


"""Euclidean Distance
"""
#The distance between the current cell and the goal cell using the distance formula

def heuristic_2(current_cell, goal):
    return sqrt ((current_cell[0] - goal[0])**2 + (current_cell[1] - goal[1])**2)