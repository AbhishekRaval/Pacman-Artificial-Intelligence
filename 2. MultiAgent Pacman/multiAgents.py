# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        # chosenIndex = max(bestIndices)

        "Add more of your code here if you want to"
        # print scores
        # print "scores above"
        # print bestScore
        # print "bestscore above"

        # print bestIndices
        # print "bestIndices above"
        # print  legalMoves[chosenIndex]

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        #Documentation of evaluation_function:
        """
        Problem Stated: : As features, try the reciprocal of important values (such as distance to food) rather than just the values
        themselves.
        
        1. So First of All I extracted all the requirements, it was required to create a evaluation function.
           Evaluation funnction was supposed to return the score, that was explicit and the computation should be on the 
           basis of some factor.
        2. CurrentPacmanposition, foodlist, and ghosts were alrerady pre-existing. Stored Ghost locations and it's 
           scaretime in Ghosts_manhattandist_scaredtimer multidimensional list, where each node's first element is location
           of ghost and second element is it's scarytime.
           so Ghosts_manhattandist_scaredtimer= [(ghostlocation,scaredtime)...n] for all items.
        3. My  evaluation function works by taking 4 factors into consideration.
            -> Inversed Manhattan distance from current location of pacman to food
            -> Distance from ghost and whether the ghost is in scarystate, i.e whether ghosts are eatable or
               they'll end the game and computed score on the basis of that. +1000 when the ghost is eatable, since that 
               leads to the maximum score and -100 when the ghosts are near, and since that situation can end the game,
               negated it's score. 
            -> length of the foodlist (empirical analysis of adding this component made the code more efficient)
            -> Succescorscore, my total addition was summation of all the above components.
        4. Achieved some of the values, by empirical testing of evaluationfunction.    
               
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # CONSTANTS:
        "*** YOUR CODE HERE ***"

        # increment for ghost not near and scaredtime is on, i.e eatable ghosts
        GHOST_SCARED = 1000
        # decrerment time for ghosts not scared
        GHOST_ACTIVE = 100
        # constant for finding food inverse of manhattan distance
        FOOD_INVERSE = 1.5

        CurrentPacmanpposition = newPos;
        FoodList = newFood.asList()
        Ghostliststates = []
        Ghosts_manhattandist_scaredtimer = []
        Total_food_score = 0
        Total_ghost_score = 0

        # storing all ghosts in an GhostList, for tweaking the list without accessing original list:
        for ghost in newGhostStates:
            Ghostliststates.append(ghost)
        # storing manhattan distance and all the scaredtimer in Ghosts_manhattandist_scaredtime list.
        for i in Ghostliststates:
            ghostposition = i.getPosition()
            ghostscoretemp = manhattanDistance(ghostposition, CurrentPacmanpposition)
            scaredtimer = i.scaredTimer
            Ghosts_manhattandist_scaredtimer.append((ghostscoretemp, scaredtimer))

        for eachghost in Ghosts_manhattandist_scaredtimer:
            ghostscoretemp = eachghost[0]
            scaredtimer = eachghost[1]
            if (ghostscoretemp <= 1 and scaredtimer > 0):
                Total_ghost_score = Total_ghost_score + GHOST_SCARED
            elif (ghostscoretemp <= 1):
                Total_ghost_score = Total_ghost_score - GHOST_ACTIVE

        for food in FoodList:
            Total_food_score_temp = manhattanDistance(food, CurrentPacmanpposition)
            Total_food_score = Total_food_score + 1 / (FOOD_INVERSE * Total_food_score_temp)

        successorscore = successorGameState.getScore()
        foodlength = len(FoodList)
        Food_ghost_Scores_Total = Total_ghost_score  + Total_food_score + foodlength
        totalevaluation = successorscore + Food_ghost_Scores_Total

        # print newFood
        # print "foodabove"
        # print newPos
        # print "pacman pos"
        # print newGhostStates
        # print  "ghost state above"
        # print successorGameState.getScore()
        # print "getscore that is returned"

        "*** YOUR CODE HERE ***"
        return totalevaluation


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):

    "*** YOUR CODE HERE ***"
    """ """

    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):

        #used Minimax pseudocode from slide.

        ##we'll check if the current state is pacman's state and if it' true,
        # returns action for current
        Pacmans_current_state = gameState
        # agentIndex = 0 means Pacman, i.e pacman position resides at depth 0
        # ghosts reside at depths>1
        Pacmans_depth = 0
        Current_index = self.index
        Permissible_Actions = []

        # getting state value by recursively calling, value, max and min.
        Pacman_state_value = self.value(Pacmans_current_state, Pacmans_depth, self.index)
        Pacman_action = Pacman_state_value[1]
        # we'll return given state's action
        return Pacman_action

    def value(self, gameState, CurrentDepth, agentIndex):
        currentAgentIndex = agentIndex
        currentState = gameState
        totalAgents = currentState.getNumAgents()
        GetDepth = CurrentDepth
        Permissible_Actions = []
        selfdepth = self.depth

        # given state is non-terminal, so we'll go to it's depth recursively
        if (currentAgentIndex == totalAgents):
            GetDepth = GetDepth + 1
            currentAgentIndex = 0

        Permissible_Actions = currentState.getLegalActions(currentAgentIndex)
        Is_Empty_corners_list = list(Permissible_Actions)

        # given state is terminal, so we'll return it's state
        #there are four conditions for given state to be terminal
        """ 
        -> if the game is lost.
        -> if the game is won.
        -> if there are no more depths left in program to be traversed
        -> if the list for Permissible Actions, i.e currentState.getLegalActions(currentAgentIndex)
           is empty.
        """
        if(currentState.isLose()
            or currentState.isWin()
            or (GetDepth == selfdepth)
            or not Is_Empty_corners_list):

            Current_Plausible_Value = self.evaluationFunction(currentState)
            return [Current_Plausible_Value]

        if (currentAgentIndex == 0):
            #agent is max for pacman, so if it indexes to 0, we'll return max, else min
            return self.max_value(currentState, GetDepth, currentAgentIndex)
        else:
            #for index>1 are states for ghosts, thus we'll return min for those states
            return self.min_value(currentState, GetDepth, currentAgentIndex)


    def min_value(self, gameState, CurrentDepth, agentIndex):

        MAXIMUM_NODE_VALUE = [float("inf")]

        #initialize v = +infinity
        Current_Value_In_State = MAXIMUM_NODE_VALUE
        currentAgentIndex = agentIndex
        currentState = gameState
        GetDepth = CurrentDepth
        Permissible_Actions = []

        Permissible_Actions = gameState.getLegalActions(currentAgentIndex)
        Length_Permissible_Actions = len(Permissible_Actions)

        for permissible_action in Permissible_Actions:

            Current_Leaf_Successor = currentState.generateSuccessor(currentAgentIndex, permissible_action)
            Leaf_Value = self.value(Current_Leaf_Successor, GetDepth, currentAgentIndex + 1)
            # for each successor state:
            # v = min(v,value of successor)
            Leaf_Value = Leaf_Value[0]

            if (Leaf_Value < Current_Value_In_State[0]):
                Current_Value_In_State = [Leaf_Value, permissible_action]
        #return current minimum value
        return Current_Value_In_State

    def max_value(self, gameState, CurrentDepth, agentIndex):

        MINIMUM_NODE_VALUE = [-float("inf")]
        # initialize v = -infinity
        Current_Value_In_State = MINIMUM_NODE_VALUE
        currentAgentIndex = agentIndex
        currentState = gameState
        GetDepth = CurrentDepth
        Permissible_Actions = []

        Permissible_Actions = gameState.getLegalActions(currentAgentIndex)
        Length_Permissible_Actions = len(Permissible_Actions)

        for permissible_action in Permissible_Actions:
            Current_Leaf_Successor = currentState.generateSuccessor(currentAgentIndex, permissible_action)
            Leaf_Value = self.value(Current_Leaf_Successor, GetDepth, currentAgentIndex + 1)
            # for each successor state:
            # v = max(v,value of successor)
            Leaf_Value = Leaf_Value[0]

            if (Leaf_Value > Current_Value_In_State[0]):
                Current_Value_In_State = [Leaf_Value, permissible_action]

        # return current maximum value
        return Current_Value_In_State





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # used alpha-beta pruning pseudocode from slide.

        ##we'll check if the current state is pacman's state and if it' true,
        # returns action for current
        Pacmans_current_state = gameState
        # agentIndex = 0 means Pacman, i.e pacman position resides at depth 0
        # ghosts reside at depths>1
        Pacmans_depth = 0
        Current_index = self.index
        Permissible_Actions = []


        # gettin state value by recursively calling, Alpha_beta_value, max and min.

        Pacman_state_value = self.Alpha_Beta_value(Pacmans_current_state, Pacmans_depth, self.index, -float("inf"), float("inf"))
        Pacman_action = Pacman_state_value[1]

        # we'll return given state's action
        return Pacman_action

    def Alpha_Beta_value(self, gameState, CurrentDepth, agentIndex, alpha, beta):

        # used new variables, for simpler implementation of algorithm
        currentAgentIndex = agentIndex
        currentState = gameState
        totalAgents = currentState.getNumAgents()
        GetDepth = CurrentDepth
        Permissible_Actions = []
        selfdepth = self.depth

        # given state is non-terminal, so we'll go to it's depth recursively

        if (currentAgentIndex == totalAgents):
            GetDepth = GetDepth + 1
            currentAgentIndex = 0

        Permissible_Actions = gameState.getLegalActions(currentAgentIndex)
        Is_Empty_corners_list = list(Permissible_Actions)

        # given state is terminal, so we'll return it's action
        #there are four conditions for given state to be terminal
        """ 
        -> if the game is lost.
        -> if the game is won.
        -> if there are no more depths left in program to be traversed
        -> if the list for Permissible Actions, i.e currentState.getLegalActions(currentAgentIndex)
           is empty.
        """


        if (currentState.isLose()
            or currentState.isWin()
            or (GetDepth == selfdepth)
            or not Is_Empty_corners_list):
            Current_Plausible_Value = self.evaluationFunction(currentState)
            return [Current_Plausible_Value]

        if (currentAgentIndex == 0):
            # agent is max for pacman, so if it indexes to 0, we'll return max, else min
            return self.max_value(currentState, GetDepth, currentAgentIndex, alpha, beta)
        else:
            # for index>1 are states for ghosts, thus we'll return min for those states
            return self.min_value(currentState, GetDepth, currentAgentIndex, alpha, beta)

    def max_value(self, gameState, CurrentDepth, agentIndex, alpha, beta):

        MINIMUM_NODE_VALUE = [-float("inf")]
        # initialize v = -infinity
        Current_Value_In_State = MINIMUM_NODE_VALUE
        currentAgentIndex = agentIndex
        currentState = gameState
        GetDepth = CurrentDepth
        Permissible_Actions = []

        Permissible_Actions = gameState.getLegalActions(currentAgentIndex)
        Length_Permissible_Actions = len(Permissible_Actions)

        for permissible_action in Permissible_Actions:
            Current_Leaf_Successor = currentState.generateSuccessor(currentAgentIndex, permissible_action)
            Leaf_Value = self.Alpha_Beta_value(Current_Leaf_Successor, GetDepth, currentAgentIndex + 1, alpha, beta)
            # for each successor state:
            # v = max(v,value of successor)
            Leaf_Value = Leaf_Value[0]

            if (Leaf_Value > Current_Value_In_State[0]):
                Current_Value_In_State = [Leaf_Value, permissible_action]

            Current_max_value = Current_Value_In_State[0]

            if Current_max_value > beta:
                return Current_Value_In_State
            # alpha = max(v,alpha)
            alpha = max(Current_max_value, alpha)

        # return current maximum value
        return Current_Value_In_State

    def min_value(self, gameState, CurrentDepth, agentIndex, alpha, beta):

        MAXIMUM_NODE_VALUE = [float("inf")]

        #initialize v = +infinity
        Current_Value_In_State = MAXIMUM_NODE_VALUE
        currentAgentIndex = agentIndex
        currentState = gameState
        GetDepth = CurrentDepth
        Permissible_Actions = []

        Permissible_Actions = gameState.getLegalActions(currentAgentIndex)
        Length_Permissible_Actions = len(Permissible_Actions)

        for permissible_action in Permissible_Actions:
            Current_Leaf_Successor = currentState.generateSuccessor(currentAgentIndex, permissible_action)
            Leaf_Value = self.Alpha_Beta_value(Current_Leaf_Successor, GetDepth, currentAgentIndex + 1, alpha, beta)
            # for each successor state:
            # v = min(v,value of successor)
            Leaf_Value = Leaf_Value[0]

            if (Leaf_Value < Current_Value_In_State[0]):
                Current_Value_In_State = [Leaf_Value, permissible_action]

            Current_min_value = Current_Value_In_State[0]

            if Current_min_value < alpha:
                return Current_Value_In_State

            #beta = min(v,beta)

            beta = min(Current_min_value, beta)
        # return current minimum value
        return Current_Value_In_State

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):

        # used Expectimax pseudocode from slide.

        ##we'll check if the current state is pacman's state and if it' true,
        # returns action for current
        Pacmans_current_state = gameState
        # agentIndex = 0 means Pacman, i.e pacman position resides at depth 0
        # ghosts reside at depths>1
        Pacmans_depth = 0
        Current_index = self.index
        Permissible_Actions = []

        # gettin state value by recursively calling, ExpectiMax_value, max and expect.
        Pacman_state_value = self.ExpectiMax_value(Pacmans_current_state, Pacmans_depth, self.index)
        Pacman_action = Pacman_state_value[1]
        #we'll return given state's action
        return Pacman_action

    def ExpectiMax_value(self, gameState, CurrentDepth, agentIndex):
        currentAgentIndex = agentIndex
        currentState = gameState
        totalAgents = currentState.getNumAgents()
        GetDepth = CurrentDepth
        Permissible_Actions = []
        selfdepth = self.depth

        if (currentAgentIndex == totalAgents):
            GetDepth = GetDepth + 1
            currentAgentIndex = 0

        Permissible_Actions = currentState.getLegalActions(currentAgentIndex)
        Is_Empty_corners_list = list(Permissible_Actions)

        if (currentState.isLose()
            or currentState.isWin()
            or (GetDepth == selfdepth)
            or not Is_Empty_corners_list):
            Current_Plausible_Value = self.evaluationFunction(currentState)
            return [Current_Plausible_Value]

        if (currentAgentIndex == 0):
            return self.max_value(currentState, GetDepth, currentAgentIndex)
        else:
            return self.exp_value(currentState, GetDepth, currentAgentIndex)

    def exp_value(self, gameState, CurrentDepth, agentIndex):
        MAXIMUM_NODE_VALUE = [float("inf")]
        # initialize v = +infinity
        Current_Value_In_State = 0
        currentAgentIndex = agentIndex
        currentState = gameState
        GetDepth = CurrentDepth
        Permissible_Actions = []
        #value list to store all the probability values
        values = []

        Permissible_Actions = currentState.getLegalActions(currentAgentIndex)
        #Length_Permissible_Actions = len(Permissible_Actions)

        #probValue = 1.0 / Length_Permissible_Actions

        for permissible_action in Permissible_Actions:
            Current_Leaf_Successor = currentState.generateSuccessor(currentAgentIndex, permissible_action)
            Leaf_Value = self.ExpectiMax_value(Current_Leaf_Successor, GetDepth, currentAgentIndex + 1)
            # for each successor state:
            #p=probability(successor)
            #v+=p*value(successor)
            Leaf_Value = Leaf_Value[0]
            values.append(Leaf_Value)

        sum_of_all_values = sum(values)
        len_sum = len(values)
        Leaf_Value = sum_of_all_values / len_sum

        Current_Value_In_State = [Leaf_Value, permissible_action]
        #return vl
        return Current_Value_In_State

    def max_value(self, gameState, CurrentDepth, agentIndex):

        MINIMUM_NODE_VALUE = [-float("inf")]
        # initialize v = -infinity
        Current_Value_In_State = MINIMUM_NODE_VALUE
        currentAgentIndex = agentIndex
        currentState = gameState
        GetDepth = CurrentDepth
        Permissible_Actions = []


        Permissible_Actions = gameState.getLegalActions(currentAgentIndex)
        Length_Permissible_Actions = len(Permissible_Actions)

        for permissible_action in Permissible_Actions:
            Current_Leaf_Successor = currentState.generateSuccessor(currentAgentIndex, permissible_action)
            Leaf_Value = self.ExpectiMax_value(Current_Leaf_Successor, GetDepth, currentAgentIndex + 1)

            # for each successor state:
            # v = max(v,value of successor)
            Leaf_Value = Leaf_Value[0]
            if (Leaf_Value > Current_Value_In_State[0]):
                Current_Value_In_State = [Leaf_Value, permissible_action]

        # return current maximum value
        return Current_Value_In_State


def betterEvaluationFunction(currentGameState):
    # Useful information you can extract from a GameState (pacman.py)
    """
       Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
       evaluation function (question 5).
       DESCRIPTION: <write something here so we know what you did>
     """


    "*** YOUR CODE HERE ***"

    """
    This was what I did, while improving the evaluationFunction:
    1. So First of All I extracted all the requirements, it was required to create a evaluation function.
       Evaluation funnction was supposed to return the score, that was explicit and the computation should be on the 
       basis of some factor.
    2. CurrentPacmanposition, foodlist, and ghosts were alrerady pre-existing. Stored Ghost locations and it's 
       scaretime in Ghosts_manhattandist_scaredtimer multidimensional list, where each node's first element is location
       of ghost and second element is it's scarytime.
       so Ghosts_manhattandist_scaredtimer= [(ghostlocation,scaredtime)...n] for all items.
    3. My  evaluation function works by taking 4 factors into consideration.
        -> Inversed Manhattan distance from current location of pacman to food
        -> Distance from ghost and whether the ghost is in scarystate, i.e whether ghosts are eatable or
           they'll end the game and computed score on the basis of that. +1000 when the ghost is eatable, since that 
           leads to the maximum score and -100 when the ghosts are near, and since that situation can end the game,
           negated it's score. 
        -> length of the foodlist (empirical analysis of adding this component made the code more efficient)
        -> Succescorscore, my total addition was summation of all the above components.
    4. Achieved some of the values, by empirical testing of evaluationfunction.
    """

    """
    This was what I did, while improving the evaluationFunction in making betterevaluationfunction:
    Used the majority of logic same, as it was in above evaluation function, with following tweaks:
    1. Ghost function was same, in foodheuristic, I tried dividing tempmanhattandistance, but the function worsened
      so multiplied, the tempmanhattandistance with itself and it improved the algorithm.
    2.     Food_ghost_Scores_Total = Total_ghost_score*0.5  + Total_food_score*0.5 + foodlength*2
            totalevaluation = successorscore*0.2 + Food_ghost_Scores_Total*0.8 
      This was the major change in code, where I gave weightage to each compnents, on the basis of empirical analysis,
      by trying multiple combinations, this led to best optimal solution, where totalevaluation is based majorly on successorscore
      and distance total for manhattan,food and twice food length. 
      Weightage of system:
        successorscore = 20% of the overall weightage score.
        Food_ghost_Scores_Total = 80% of the overall weightage score.
         where,
            Total_ghost_score & Total_food_score = 33.33% of weightage of Food_ghost_Scores_Total
            Foodlist's length = 66.66% of weightage of Food_ghost_Scores_Total      
    
    """

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # CONSTANTS:
    "*** YOUR CODE HERE ***"

    # increment for ghost not near and scaredtime is on, i.e eatable ghosts
    GHOST_SCARED = 1000
    # decrerment time for ghosts not scared
    GHOST_ACTIVE = 100
    # constant for finding food inverse of manhattan distance
    FOOD_INVERSE = 1.5

    CurrentPacmanpposition = newPos;
    FoodList = newFood.asList()
    Ghostliststates = []
    Ghosts_manhattandist_scaredtimer = []
    Total_food_score = 0
    Total_ghost_score = 0

    # storing all ghosts in an GhostList, for tweaking the list without accessing original list:
    for ghost in newGhostStates:
        Ghostliststates.append(ghost)
    # storing manhattan distance and all the scaredtimer in Ghosts_manhattandist_scaredtime list.
    for i in Ghostliststates:
        ghostposition = i.getPosition()
        ghostscoretemp = manhattanDistance(ghostposition, CurrentPacmanpposition)
        scaredtimer = i.scaredTimer
        Ghosts_manhattandist_scaredtimer.append((ghostscoretemp, scaredtimer))

    for eachghost in Ghosts_manhattandist_scaredtimer:
        ghostscoretemp = eachghost[0]
        scaredtimer = eachghost[1]
        if (ghostscoretemp <= 1 and scaredtimer > 0):
            Total_ghost_score = Total_ghost_score + GHOST_SCARED
        elif (ghostscoretemp <= 1):
            Total_ghost_score = Total_ghost_score - GHOST_ACTIVE

    for food in FoodList:
        Total_food_score_temp = manhattanDistance(food, CurrentPacmanpposition)
        Total_food_score_temp = Total_food_score_temp *Total_food_score_temp
        Total_food_score = Total_food_score + 1 / (FOOD_INVERSE*Total_food_score_temp)

    successorscore = currentGameState.getScore()
    foodlength = len(FoodList)
    Food_ghost_Scores_Total = Total_ghost_score*0.5  + Total_food_score*0.5 + foodlength*2
    totalevaluation = successorscore*0.2 + Food_ghost_Scores_Total*0.8

    return totalevaluation


# Abbreviation
better = betterEvaluationFunction
