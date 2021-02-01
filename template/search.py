# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

from queue import Queue
from queue import PriorityQueue
from copy import copy

class State:
    def __init__(self, row, col, objectives, parent=None):
        self.__row = row
        self.__col = col
        self.__objectives = objectives
        self.__parent = parent
        self.__fFunction = 0

    def __eq__(self, other):
        return (self.__row == other.__row and self.__col == other.__col and self.__objectives == other.__objectives)

    def __hash__(self):
        return (hash(str(self.__row) + str(self.__col) + str(len(self.__objectives))))

    def __lt__(self, other):
        return (self.__fFunction < other.__fFunction)

    # returns coordinates of current cell
    def cell(self):
        return (self.__row, self.__col) 
    
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
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
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
            # if len(objectivesLeft) == 0:
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

    return ret
    


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    gFunction = {}
    frontier = PriorityQueue()
    path = []
    ret = []
    objectives = maze.getObjectives()
    start = State(maze.getStart()[0], maze.getStart()[1], objectives[0])
    gFunction[start] = 0
    frontier.put(start)

    while not frontier.empty():

        currentState = frontier.get()
        currentCell = currentState.cell()

        # objective found, initialise backtrace and exit search
        if maze.isObjective(currentCell[0], currentCell[1]):

            path.append(currentState)
            ret.append(currentCell)
            break

        neighbors = maze.getNeighbors(currentCell[0], currentCell[1])

        for i in neighbors:

            neighbor = State(i[0], i[1], objectives[0])
            gVal= gFunction[currentState]+1

            # if neighbor is not visited or if we found better path to it, add it to the frontier
            if neighbor not in gFunction or gVal < gFunction[neighbor]:
                neighbor.setParent(currentState)
                gFunction[neighbor] = gVal
                hFunction = abs(objectives[0][0] - i[0]) + abs(objectives[0][1] - i[1]) # use manhatten distance as heuristic
                neighbor.setfFunction(gFunction[neighbor] + hFunction)
                frontier.put(neighbor)

    # backtrace
    while path[0]!= start:
        
        currentCell = path[0]
        path.insert(0, currentCell.parent())
        ret.insert(0, currentCell.parent().cell())

    return ret

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.
        
    @param maze: The maze to execute the search on.
        
    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    gFunction = {}
    frontier = PriorityQueue()
    path = []
    ret = []
    objectives = maze.getObjectives()
    start = State(maze.getStart()[0], maze.getStart()[1], objectives)
    gFunction[start] = 0
    frontier.put(start)

    while not frontier.empty():

        currentState = frontier.get()
        currentCell = currentState.cell()
        objectivesLeft = currentState.objectives()

        if objectivesLeft.count(currentCell) != 0:
            objectivesLeft.remove(currentCell)

            # all objectives found, initialise backtrace and exit loop
            if len(objectivesLeft) == 0:
                path.clear()
                ret.clear()
                path.append(currentState)
                ret.append(currentCell)
                break

        neighbors = maze.getNeighbors(currentCell[0], currentCell[1])

        for i in neighbors:

            neighbor = State(i[0], i[1], objectivesLeft)
            gVal= gFunction[currentState] + 1

            # if neighbor is not visited or if we found better path to it, add it to the frontier
            if neighbor not in gFunction or gVal < gFunction[neighbor]:

                neighbor.setParent(currentState)
                gFunction[neighbor] = gVal

                hFunction = 0
                for j in objectivesLeft:
                    hFunction += abs(j[0] - i[0]) + abs(j[1] - i[1]) # use sum of manhatten distances to corners as heuristic

                neighbor.setfFunction(gFunction[neighbor] + hFunction)
                frontier.put(neighbor)

    # backtrace
    while path[0]!= start:
        
        currentCell = path[0]
        path.insert(0, currentCell.parent())
        ret.insert(0, currentCell.parent().cell())

    return ret
    

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    gFunction = {}
    frontier = PriorityQueue()
    path = []
    ret = []
    MSTLengths = {}
    edges = {}

    objectives = maze.getObjectives()
    start = State(maze.getStart()[0], maze.getStart()[1], objectives)
    gFunction[start] = 0
    frontier.put(start)  
    getEdgeWeights(maze, objectives, edges) # init edge weights for MST

    while not frontier.empty():

        currentState = frontier.get()
        currentCell = currentState.cell()
        objectivesLeft = currentState.objectives()

        if objectivesLeft.count(currentCell) != 0:
            objectivesLeft.remove(currentCell)

            # all objectives found, initialise backtrace and exit loop
            if len(objectivesLeft) == 0:
                path.clear()
                ret.clear()
                path.append(currentState)
                ret.append(currentCell)
                break
        
        # if we have already calculated MST length we can reuse value
        # else calculate MST length for this state and store it.
        length = 0
        if str(objectivesLeft) in MSTLengths:
            length = MSTLengths[str(objectivesLeft)]
        else:
            length = getMSTLength(objectivesLeft.copy(), maze, edges)
            MSTLengths[str(objectivesLeft)] = length

        neighbors = maze.getNeighbors(currentCell[0], currentCell[1])

        for i in neighbors:

            neighbor = State(i[0], i[1], objectivesLeft)
            gVal= gFunction[currentState] + 1

            if neighbor not in gFunction or gVal < gFunction[neighbor]:

                neighbor.setParent(currentState)
                gFunction[neighbor] = gVal

                hFunction = []
                for j in objectivesLeft:
                    hFunction.append(abs(j[0] - i[0]) + abs(j[1] - i[1]) + length) # use MST length + manhatten distance to nearest objective as heuristic.

                hVal = min(hFunction)

                neighbor.setfFunction(gFunction[neighbor] + hVal)
                frontier.put(neighbor)

    # backtrace
    while path[0]!= start:
        
        currentCell = path[0]
        path.insert(0, currentCell.parent())
        ret.insert(0, currentCell.parent().cell())

    return ret

def getMSTLength(objectives, maze, edges):

    length = 0
    curr = objectives[0]
    objectivesFound = []
    maxLength = maze.getDimensions()[0] + maze.getDimensions()[1]

    while len(objectives) != 0:

        # move node from unvistited to visited
        objectives.remove(curr)
        objectivesFound.append(curr)
        pathLength = maxLength

        for j in objectivesFound:
            for i in objectives:
                temp = edges[(i,j)] # get edge length
                if temp < pathLength:
                    pathLength = temp
                    curr = i

        length += pathLength  
        
    return length

def getEdgeWeights(maze, objectives, edges):
 
    for j in objectives:
        for i in objectives:
            if i != j:
                tempMaze = copy(maze)
                tempMaze.setStart(j)
                tempMaze.setObjectives([i])
                temp = len(astar(tempMaze)) # use astar single to get edge weight
                edges[(i,j)] = temp
                
def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
