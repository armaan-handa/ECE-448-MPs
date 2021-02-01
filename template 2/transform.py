
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    limits = arm.getArmLimit()
    width = (limits[0][1] - limits[0][0])/granularity
    width = int(width)
    width += 1

    height = (limits[1][1] - limits[1][0])/granularity
    height = int(height)
    height += 1

    offsets = [limits[i][0] for i in range(len(limits))]

    startingPoint = arm.getArmAngle()
    maze_map = [[None for i in range(height)] for j in range(width)]
    x, y = angleToIdx(startingPoint, offsets, granularity)
    maze_map[x][y] = START_CHAR

    for a in range(limits[0][0], limits[0][1] + 1, granularity):
        for b in range(limits[1][0], limits[1][1] + 1, granularity):
            x, y = angleToIdx((a,b), offsets, granularity)
            if maze_map[x][y] != None:
                continue
            arm.setArmAngle([a, b])
            if doesArmTouchObjects(arm.getArmPosDist(), obstacles) or \
                (doesArmTouchObjects(arm.getArmPosDist(), goals, True) and (not doesArmTipTouchGoals(arm.getEnd(), goals))) or\
                    not isArmWithinWindow(arm.getArmPos(), window):
                    maze_map[x][y] = WALL_CHAR
            elif doesArmTipTouchGoals(arm.getEnd(), goals):
                maze_map[x][y] = OBJECTIVE_CHAR
            else:
                maze_map[x][y] = SPACE_CHAR


    maze = Maze(maze_map, offsets, granularity)

    return maze