# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush
from queue import Queue
from copy import copy
from util import *

class State:

    def __init__(self, alpha, beta, objectives, parent=None):
        self.__alpha = alpha
        self.__beta = beta
        self.__objectives = objectives
        self.__parent = parent
        self.__fFunction = 0

    def __eq__(self, other):
        return (self.__alpha == other.__alpha and self.__beta == other.__beta and self.__objectives == other.__objectives)

    def __hash__(self):
        return (hash(str(self.__alpha) + str(self.__beta) + str(len(self.__objectives))))

    def __lt__(self, other):
        return (self.__fFunction < other.__fFunction)

    # returns coordinates of current cell
    def cell(self):
        return (self.__alpha, self.__beta) 
    
    # returns list of remaining objectives in current state
    def objectives(self):
        return self.__objectives.copy()
    
    #returns State object containing parent of current state
    def parent(self):
        return self.__parent
    
    def setfFunction(self, fFunction):
        self.__fFunction = fFunction
    
    def setParent(self, parent):
        self.__parent = parent

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None. 
    """
    frontier = Queue()
    visited = []
    path = []
    ret = []
    objectives = maze.getObjectives()
    start = State(maze.getStart()[0], maze.getStart()[1], objectives.copy())
    frontier.put(start)
    explored = []
    

    while not frontier.empty(): # while frontier queue is not empty

        currentState = frontier.get()
        currentCell = currentState.cell()
        objectivesLeft = currentState.objectives()

        if  objectivesLeft.count(currentCell) != 0:

            objectivesLeft.remove(currentCell)
            
            # all objectives found, initialise backtrace and exit loop
            path.append(currentState)
            ret.append(currentCell)
            visited.append(currentState)
            break

        # current cell is not objective nor visited
        if visited.count(currentState) == 0:
            explored.append(currentCell)
            neighbors = maze.getNeighbors(currentCell[0], currentCell[1])

            for i in neighbors:

                neighbor = State(i[0], i[1], objectivesLeft)

                # if neighbor is not visited, add it to the frontier
                if visited.count(neighbor) == 0:
                    neighbor.setParent(currentState)
                    frontier.put(neighbor)

            visited.append(currentState)

    #backtrace
    while path[0] != start:

        currentState = path[0]
        path.insert(0, currentState.parent())
        ret.insert(0, currentState.parent().cell())

    if ret == []:
        return None
    return ret
