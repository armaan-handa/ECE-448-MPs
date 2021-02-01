# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position (int,int):of the arm link, (x-coordinate, y-coordinate)
    """
    x = length * np.cos(np.deg2rad(angle))
    y = length * np.sin(np.deg2rad(angle))
    x = int(x)
    y = int(y)
    x += start[0]
    y = start[1] - y
    
    return (x, y)

def doesArmTouchObjects(armPosDist, objects, isGoal=False):
    """Determine whether the given arm links touch any obstacle or goal

        Args:
            armPosDist (list): start and end position and padding distance of all arm links [(start, end, distance)]
            objects (list): x-, y- coordinate and radius of object (obstacles or goals) [(x, y, r)]
            isGoal (bool): True if the object is a goal and False if the object is an obstacle.
                           When the object is an obstacle, consider padding distance.
                           When the object is a goal, no need to consider padding distance.
        Return:
            True if touched. False if not.
    """
    for link in armPosDist:
        startPos = link[0]
        endPos = link[1]
        padding = link[2]

        for obj in objects:
            # get start and end of link relative to center of object 
            relativeStart = (startPos[0] - obj[0], obj[1] - startPos[1]) 
            relativeEnd = (endPos[0] - obj[0], obj[1] - endPos[1])

            # variables needed for checking intersections
            dx = relativeEnd[0] - relativeStart[0]
            dy = relativeEnd[1] - relativeStart[1]
            dr = np.sqrt(dx**2 + dy**2)
            D = relativeStart[0] * relativeEnd[1] - relativeStart[1] * relativeEnd[0]
            r = obj[2] if isGoal else obj[2] + padding

            delta = (r**2)*(dr**2) - D**2

            if delta >= 0:
                x1 = (D*dy + np.sign(dy)*dx*np.sqrt(delta))/(dr**2)
                x2 = (D*dy - np.sign(dy)*dx*np.sqrt(delta))/(dr**2)
                y1 = (-D*dx + np.absolute(dy)*np.sqrt(delta))/(dr**2)
                y2 = (-D*dx - np.absolute(dy)*np.sqrt(delta))/(dr**2)
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
                if  ((x1 > relativeStart[0] and x1 >relativeEnd[0]) or (x1 < relativeStart[0] and x1 < relativeEnd[0]) \
                        or (y1 > relativeStart[1] and y1 >relativeEnd[1]) or (y1 < relativeStart[1] and y1 < relativeEnd[1])) \
                            and ((x2 > relativeStart[0] and x2 >relativeEnd[0]) or (x2 < relativeStart[0] and x2 < relativeEnd[0]) \
                                or (y2 > relativeStart[1] and y2 >relativeEnd[1]) or (y2 < relativeStart[1] and y2 < relativeEnd[1])):
                        continue
                return True

    return False

def doesArmTipTouchGoals(armEnd, goals):
    """Determine whether the given arm tip touch goals

        Args:
            armEnd (tuple): the arm tip position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]. There can be more than one goal.
        Return:
            True if arm tick touches any goal. False if not.
    """
    for goal in goals:
        relativeX = goal[0] - armEnd[0]
        relativeY = goal[1] - armEnd[1]
        if np.sqrt((relativeX**2) + (relativeY**2)) <= goal[2]:
            return True

    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end positions of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False if not.
    """
    for link in armPos:
        start = link[0]
        end = link[1]
        if start[0] < 0 or start[0] > window[0] or start[1] < 0 or start[1] > window[1] or end[0] < 0 or end[0] > window[0] or end[1] < 0 or end[1] > window[1]:
            return False

    return True


if __name__ == '__main__':
    computeCoordinateParameters = [((150, 190),100,20), ((150, 190),100,40), ((150, 190),100,60), ((150, 190),100,160)]
    resultComputeCoordinate = [(243, 156), (226, 126), (200, 104), (57, 156)]
    testRestuls = [computeCoordinate(start, length, angle) for start, length, angle in computeCoordinateParameters]
    assert testRestuls == resultComputeCoordinate

    testArmPosDists = [((100,100), (135, 110), 4), ((135, 110), (150, 150), 5)]
    testObstacles = [[(120, 100, 5)], [(110, 110, 20)], [(160, 160, 5)], [(130, 105, 10)]]
    resultDoesArmTouchObjects = [
        True, True, False, True, False, True, False, True,
        False, True, False, True, False, False, False, True
    ]

    testResults = []
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle))

    print("\n")
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
    assert resultDoesArmTouchObjects == testResults

    testArmEnds = [(100, 100), (95, 95), (90, 90)]
    testGoal = [(100, 100, 10)]
    resultDoesArmTouchGoals = [True, True, False]

    testResults = [doesArmTipTouchGoals(testArmEnd, testGoal) for testArmEnd in testArmEnds]
    assert resultDoesArmTouchGoals == testResults

    testArmPoss = [((100,100), (135, 110)), ((135, 110), (150, 150))]
    testWindows = [(160, 130), (130, 170), (200, 200)]
    resultIsArmWithinWindow = [True, False, True, False, False, True]
    testResults = []
    for testArmPos in testArmPoss:
        for testWindow in testWindows:
            testResults.append(isArmWithinWindow([testArmPos], testWindow))
    assert resultIsArmWithinWindow == testResults

    print("Test passed\n")
