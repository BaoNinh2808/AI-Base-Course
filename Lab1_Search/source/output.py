import os
from a_star import *
from gfbs import *
from heuristic import *
from bfs import *
from ucs import *
from dfs import *

def write_ouput_txt_file(route, txt_path):
    cost = len(route)
    if os.path.exists(txt_path):    #delete the old one
        os.remove(txt_path)

    f = open(txt_path,'w')
    if (cost == 0):
        f.write("NO")
    else:
        f.write(str(cost))
    f.close()

def outputBFS(matrix, bonus_points, start, goal, outputPath):
    bfsOutPath = os.path.join(outputPath, 'bfs')
    os.makedirs(bfsOutPath, exist_ok=True)

    path, visit_list = bfs(matrix, start, goal)

    txt_path = os.path.join(bfsOutPath, "bfs.txt")
    write_ouput_txt_file(path, txt_path)

    video_path = os.path.join(bfsOutPath, "bfs.mp4")
    visualize_video(matrix, bonus_points, start, goal, visit_list=visit_list, path=path, outPath= video_path)

def outputDFS(matrix, bonus_points, start, goal, outputPath):
    dfsOutPath = os.path.join(outputPath, 'dfs')
    os.makedirs(dfsOutPath, exist_ok=True)

    path, visit_list = dfs(matrix, start, goal)

    txt_path = os.path.join(dfsOutPath, "dfs.txt")
    write_ouput_txt_file(path, txt_path)

    video_path = os.path.join(dfsOutPath, "dfs.mp4")
    visualize_video(matrix, bonus_points, start, goal, visit_list=visit_list, path=path, outPath= video_path)
    
def outputUCS(matrix, bonus_points, start, goal, outputPath):
    ucsOutPath = os.path.join(outputPath, 'ucs')
    os.makedirs(ucsOutPath, exist_ok=True)

    path, visit_list = ucs(matrix, start, goal)

    txt_path = os.path.join(ucsOutPath, "ucs.txt")
    write_ouput_txt_file(path, txt_path)

    video_path = os.path.join(ucsOutPath, "ucs.mp4")
    visualize_video(matrix, bonus_points, start, goal, visit_list=visit_list, path=path, outPath= video_path)

def outputGBFS(matrix, bonus_points, start, goal, outputPath):
    gbfsOutPath = os.path.join(outputPath, 'gbfs')
    os.makedirs(gbfsOutPath, exist_ok=True)

    path_1, visit_list_1 = gbfs(matrix, bonus_points, start, goal, heuristic_1)
    path_2, visit_list_2 = gbfs(matrix, bonus_points, start, goal, heuristic_2)

    txt_path_1 = os.path.join(gbfsOutPath, "gbfs_heuristic_1.txt")
    write_ouput_txt_file(path_1, txt_path_1)
    txt_path_2 = os.path.join(gbfsOutPath, "gbfs_heuristic_2.txt")
    write_ouput_txt_file(path_2, txt_path_2)

    video_path_1 = os.path.join(gbfsOutPath, "gbfs_heuristic_1.mp4")
    video_path_2 = os.path.join(gbfsOutPath, "gbfs_heuristic_2.mp4")
    visualize_video(matrix, bonus_points, start, goal, visit_list=visit_list_1, path=path_1, outPath= video_path_1)
    visualize_video(matrix, bonus_points, start, goal, visit_list=visit_list_2, path=path_2, outPath= video_path_2)

def outputASTAR(matrix, bonus_points, start, goal, outputPath):
    astarOutPath = os.path.join(outputPath, 'astar')
    os.makedirs(astarOutPath, exist_ok=True)

    path_1, visit_list_1 = astar(matrix, bonus_points, start, goal, heuristic_1)
    path_2, visit_list_2 = astar(matrix, bonus_points, start, goal, heuristic_2)

    txt_path_1 = os.path.join(astarOutPath, "astar_heuristic_1.txt")
    write_ouput_txt_file(path_1, txt_path_1)
    txt_path_2 = os.path.join(astarOutPath, "astar_heuristic_2.txt")
    write_ouput_txt_file(path_2, txt_path_2)

    video_path_1 = os.path.join(astarOutPath, "astar_heuristic_1.mp4")
    video_path_2 = os.path.join(astarOutPath, "astar_heuristic_2.mp4")
    visualize_video(matrix, bonus_points, start, goal, visit_list=visit_list_1, path=path_1, outPath= video_path_1)
    visualize_video(matrix, bonus_points, start, goal, visit_list=visit_list_2, path=path_2, outPath= video_path_2)