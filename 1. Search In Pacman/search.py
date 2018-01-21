# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

#depthFirstSearch : Problem :
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #DFS requires stack, so taking frontier_stack as a stack.
    #exploredset is an empty list, which keeps track of explored nodes.
    #path covers all direction attributes, which helps in deciding final path.
    frontier_stack = util.Stack()
    exploredset = []
    path = []
    startNode = problem.getStartState()
    frontier_stack.push((startNode, []))

    while (not frontier_stack.isEmpty()):

        tempnode = frontier_stack.pop();
        tempnode_state = tempnode[0]
        tempnode_directions = tempnode[1]

        if(problem.isGoalState(tempnode_state)):
            path = tempnode_directions
            break
        if(tempnode_state not in exploredset):
            exploredset.append(tempnode_state)
            successoroftemp = problem.getSuccessors(tempnode_state)
            for leaf in successoroftemp:
                if leaf[0] not in exploredset:
                    new_direction = tempnode_directions + [leaf[1]]
                    frontier_stack.push((leaf[0],new_direction))
    return path

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    LoadingQueue = util.Queue()  # we use stack
    exploredset = []
    path = []
    startNode = problem.getStartState()
    LoadingQueue.push((startNode, []))

    while (not LoadingQueue.isEmpty()):

        tempnode = LoadingQueue.pop();
        tempnode_state = tempnode[0]
        tempnode_directions = tempnode[1]

        if (problem.isGoalState(tempnode_state)):
            path = tempnode_directions
            break
        if (tempnode_state not in exploredset):
            exploredset.append(tempnode_state)
            successoroftemp = problem.getSuccessors(tempnode_state)
            for leaf in successoroftemp:
                if leaf[0] not in exploredset:
                    new_direction = tempnode_directions + [leaf[1]]
                    LoadingQueue.push((leaf[0], new_direction))
    return path
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    LoadingQueue = util.PriorityQueue()  # we use stack
    exploredset = []
    path = []
    inti_cost =0
    startNode = problem.getStartState()
    LoadingQueue.push((startNode, [], inti_cost),inti_cost)

    while (not LoadingQueue.isEmpty()):

        tempnode = LoadingQueue.pop();
        tempnode_state = tempnode[0]
        tempnode_directions = tempnode[1]
        tempnode_priority = tempnode[2]


        if (problem.isGoalState(tempnode_state)):
            path = tempnode_directions
            break
        if (tempnode_state not in exploredset):
            exploredset.append(tempnode_state)
            successoroftemp = problem.getSuccessors(tempnode_state)
            for leaf in successoroftemp:
                if leaf[0] not in exploredset:
                    cummulative_path_cost = tempnode_priority + leaf[2] #Cummulative cost as priority
                    new_direction = tempnode_directions + [leaf[1]]
                    LoadingQueue.push((leaf[0], (new_direction), (cummulative_path_cost)), (cummulative_path_cost))
    return path

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    LoadingQueue = util.PriorityQueue()  # we use stack
    exploredset = []
    path = []
    initial_Gofn = 0
    startNode = problem.getStartState()
    initial_HofN = heuristic(startNode, problem)
    initial_FofN = initial_HofN + initial_Gofn
    LoadingQueue.push((startNode, [],initial_Gofn), (initial_FofN))

    while (not LoadingQueue.isEmpty()):

        tempnode = LoadingQueue.pop();

        tempnode_state = tempnode[0]
        tempnode_directions = tempnode[1]
        tempnode_priority = tempnode[2]

        if (problem.isGoalState(tempnode_state)):
            path = tempnode_directions
            break
        if (tempnode_state not in exploredset):
            exploredset.append(tempnode_state)
            successoroftemp = problem.getSuccessors(tempnode_state)
            for leaf in successoroftemp:
                if leaf[0] not in exploredset:
                    HofN = heuristic(leaf[0],problem)
                    GofN = tempnode_priority + leaf[2]
                    FofN = HofN + GofN   # Cummulative cost as priority
                    new_direction = tempnode_directions + [leaf[1]]
                    LoadingQueue.push((leaf[0], (new_direction), (GofN)), (FofN))
    return path
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
