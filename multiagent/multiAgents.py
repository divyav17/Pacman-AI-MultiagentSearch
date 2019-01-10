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
import sys

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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()
        nearestThreatDistance = sys.maxint
        nearestFoodDistance = sys.maxint

        for agent in newGhostStates:
            threatDist = util.manhattanDistance(newPos, agent.configuration.pos)
            nearestThreatDistance = min(threatDist,nearestThreatDistance)

        if nearestThreatDistance != 0:
            threatFactor = -10 / nearestThreatDistance
        else:
            threatFactor = -100

        if len(foodList) == 0:
            closestfood = 0
        else:
            for food in foodList:
                foodDist = util.manhattanDistance(newPos, food)
                nearestFoodDistance = min(foodDist, nearestFoodDistance)
            closestfood = -1 * nearestFoodDistance
        return closestfood + threatFactor + successorGameState.getScore() - 10 * len(foodList)

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        bestScore, bestAction = self.minimax(gameState, 0, 0)
        return bestAction

    def minimax(self, gameState, currentTurn, depth):
        numAgents = gameState.getNumAgents()
        currentTurn = currentTurn % numAgents

        if (gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState), None
        if currentTurn == 0:
            return self.maxValue(gameState, currentTurn, depth)
        else:
            return self.minValue(gameState, currentTurn, depth)

    def maxValue(self, gameState, currentTurn, depth):
        depth = depth + 1
        if depth > self.depth:
            return self.evaluationFunction(gameState), None

        bestScore = -(sys.maxint)
        successorActions = gameState.getLegalActions(currentTurn)
        for succAction in successorActions:
            successors = []
            successors.append(gameState.generateSuccessor(currentTurn, succAction))
            for successor in successors:
                bestcurrent = self.minimax(successor, currentTurn + 1, depth)[0]
                if bestScore < bestcurrent:
                    bestScore = bestcurrent
                    bestActions = succAction
        return bestScore, bestActions

    def minValue(self, gameState, currentTurn, depth):
        if depth > self.depth:
            return self.evaluationFunction(gameState), None
        bestScore = sys.maxint

        successorActions = gameState.getLegalActions(currentTurn)
        for succAction in successorActions:
            successors = []
            successors.append(gameState.generateSuccessor(currentTurn, succAction))
            for successor in successors:
                bestCurrent = self.minimax(successor, currentTurn + 1, depth)[0]
                if bestScore > bestCurrent:
                    bestScore = bestCurrent
                    bestActions = succAction
        return bestScore, bestActions

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        alpha = - sys.maxint
        beta = sys.maxint
        bestScore, bestAction = self.ABPrune(gameState, 0, 0, alpha,beta)
        return bestAction

    def ABPrune(self, gameState, currentTurn, depth,alpha,beta):
        numAgents = gameState.getNumAgents()
        currentTurn = currentTurn % numAgents

        if (gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState), None
        if currentTurn == 0:
            return self.maxValue(gameState, currentTurn, depth,alpha,beta)
        else:
            return self.minValue(gameState, currentTurn, depth,alpha,beta)

    def maxValue(self, gameState, currentTurn, depth,alpha,beta):
        depth = depth + 1
        if depth > self.depth:
            return self.evaluationFunction(gameState), None

        bestScore = -(sys.maxint)
        successorActions = gameState.getLegalActions(currentTurn)
        for succAction in successorActions:
            successors = []
            successors.append(gameState.generateSuccessor(currentTurn, succAction))
            for successor in successors:
                bestcurrent = self.ABPrune(successor, currentTurn + 1, depth,alpha,beta)[0]
                if bestScore < bestcurrent:
                    bestScore = bestcurrent
                    bestActions = succAction
                if bestScore > beta:
                    return bestScore,bestActions
                alpha = max(alpha, bestScore)
        return bestScore, bestActions

    def minValue(self, gameState, currentTurn, depth, alpha, beta):
        if depth > self.depth:
            return self.evaluationFunction(gameState), None
        bestScore = sys.maxint

        successorActions = gameState.getLegalActions(currentTurn)
        for succAction in successorActions:
            successors = []
            successors.append(gameState.generateSuccessor(currentTurn, succAction))
            for successor in successors:
                bestCurrent = self.ABPrune(successor, currentTurn + 1, depth,alpha,beta)[0]
                if bestScore > bestCurrent:
                    bestScore = bestCurrent
                    bestActions = succAction
                if bestScore < alpha:
                    return bestScore,bestActions
                beta = min(bestScore, beta)
        return bestScore, bestActions

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        bestScore, bestAction = self.expectiMax(gameState, 0, 0)
        return bestAction

    def expectiMax(self, gameState, currentTurn, depth):
        numAgents = gameState.getNumAgents()
        currentTurn = currentTurn % numAgents

        if (gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState), None
        if currentTurn == 0:
            return self.maxValue(gameState, currentTurn, depth)
        else:
            return self.expectiVal(gameState, currentTurn, depth)

    def maxValue(self, gameState, currentTurn, depth):
        depth = depth + 1
        if depth > self.depth:
            return self.evaluationFunction(gameState), None

        bestScore = -(sys.maxint)
        successorActions = gameState.getLegalActions(currentTurn)
        for succAction in successorActions:
            successors = []
            successors.append(gameState.generateSuccessor(currentTurn, succAction))
            for successor in successors:
                bestcurrent = self.expectiMax(successor, currentTurn + 1, depth)[0]
                if bestScore < bestcurrent:
                    bestScore = bestcurrent
                    bestActions = succAction
        return bestScore, bestActions

    def expectiVal(self, gameState, currentTurn, depth):
        if depth > self.depth:
            return self.evaluationFunction(gameState), None

        bestScore = 0
        successorActions = gameState.getLegalActions(currentTurn)
        for succAction in successorActions:
            successors = []
            successors.append(gameState.generateSuccessor(currentTurn, succAction))
            for successor in successors:
                p = (1 / len(successors))
                bestScore += p * (self.expectiMax(successor, currentTurn + 1, depth)[0])
                bestActions = succAction
        return bestScore, bestActions


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    capsuleList = currentGameState.getCapsules()
    newPos = currentGameState.getPacmanPosition()

    nearestFoodDistance = sys.maxint
    nearestThreatDistance = sys.maxint

    for agent in newGhostStates:
        threatDist = util.manhattanDistance(newPos, agent.configuration.pos)
        nearestThreatDistance = min(threatDist, nearestThreatDistance)

    if nearestThreatDistance != 0:
        threatFactor = -1.0 / nearestThreatDistance
    else:
        threatFactor = 0


    if len(newFood.asList()) == 0:
        closestfood = 0
    else:
        for food in newFood.asList():
            foodDist = util.manhattanDistance(newPos, food)
            nearestFoodDistance = min(foodDist, nearestFoodDistance)
        closestfood = -1 * nearestFoodDistance

    return closestfood + threatFactor + currentGameState.getScore() - 10 * len(capsuleList)



    # Abbreviation
better = betterEvaluationFunction

