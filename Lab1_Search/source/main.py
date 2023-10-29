import os
from output import *

def processInputLevel1():
    inputPath = os.path.join(os.curdir,'input/level_1')
    txt_files = os.listdir(inputPath)
    for input in txt_files:
        #read input
        bonus_points, matrix, start, goal = read_file(os.path.join(inputPath, input))

        #create output dir
        filename = os.path.basename(input)
        filename_without_extension = os.path.splitext(filename)[0]
        outputPath = os.path.join(os.curdir,'output/level_1', filename_without_extension)
        os.makedirs(outputPath, exist_ok=True)

        #output 
        outputBFS(matrix, bonus_points, start, goal, outputPath)
        outputDFS(matrix, bonus_points, start, goal, outputPath)
        outputUCS(matrix, bonus_points, start, goal, outputPath)
        outputGBFS(matrix, bonus_points, start, goal, outputPath)
        outputASTAR(matrix, bonus_points, start, goal, outputPath)

def processInputLevel2():
    inputPath = os.path.join(os.curdir,'input/level_2')
    txt_files = os.listdir(inputPath)
    for input in txt_files:
        #read input
        bonus_points, matrix, start, goal = read_file(os.path.join(inputPath, input))

        #create output dir
        filename = os.path.basename(input)
        filename_without_extension = os.path.splitext(filename)[0]
        outputPath = os.path.join(os.curdir,'output/level_2', filename_without_extension)
        os.makedirs(outputPath, exist_ok=True)

        #output
        outputPOINT_MAP(matrix, bonus_points, start, goal, outputPath)
        
#processInputLevel1()
# inputPath = os.path.join(os.curdir,'input/level_1')
# txt_files = os.listdir(inputPath)
# for input in txt_files:
#     #read input
#     bonus_points, matrix, start, goal = read_file(os.path.join(inputPath, input))
#     visualize_maze(matrix, bonus_points, start, goal, save_path="input5_level1.jpg")

processInputLevel2()