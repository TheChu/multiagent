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

        getAction chooses among the best options according to the evaluation
        function.

        Just like in the previous project, getAction takes a GameState and
        returns some Directions.X for some X in the set {North, South, West,
        East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) \
                  for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) \
                       if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are
        better.

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
        newScaredTimes = [ghostState.scaredTimer for ghostState \
                          in newGhostStates]

        "*** YOUR CODE HERE ***"
        height, width = currentGameState.getWalls().height,\
                        currentGameState.getWalls().width
        maxPossibleDist = max(height, width)

        foodLeftBefore = len(currentGameState.getFood().asList())

        foodList = newFood.asList()
        foodLeft = len(foodList)

        # If there is no food left we win, so we choose this action regardless
        if foodLeft == 0:
            return 2 * maxPossibleDist + 1

        # Get the Manhattan distance to the closest food pellet
        foodManhattans = map(lambda xy:
                            abs(newPos[0] - xy[0]) + abs(newPos[1] - xy[1]),
                            foodList)
        closestFoodDist = min(foodManhattans)

        # Get the Manhattan distance to the closest ghost
        ghostManhattans = map(lambda xy:
                            abs(newPos[0] - xy.getPosition()[0]) \
                            + abs(newPos[1] - xy.getPosition()[1]),
                            newGhostStates)
        closestGhostDist = min(ghostManhattans)

        # We want to avoid being too close to the ghost
        if closestGhostDist < 2:
            return 0

        # We want to eat
        elif foodLeft < foodLeftBefore:
            return maxPossibleDist + maxPossibleDist / closestFoodDist

        # We want to head towards the closest food pellet
        else:
            return maxPossibleDist / closestFoodDist

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

      Note: this is an abstract class: one that should not be instantiated. It's
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

    def getActionHelper(self, gameState, agentIndex, depth):
        if (depth == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), 0

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(agentIndex)
        states = [gameState.generateSuccessor(agentIndex, action) \
                  for action in legalMoves]

        # Recursively collect scores for every successor state
        if agentIndex < gameState.getNumAgents() - 1:
            scores = [self.getActionHelper(state, agentIndex + 1, depth)[0] \
                      for state in states]
        else:
            scores = [self.getActionHelper(state, 0, depth - 1)[0] \
                      for state in states]

        # Choose best score according to current agent
        if agentIndex == 0:
            bestScore = max(scores)

            bestIndices = [index for index in range(len(scores)) \
                           if scores[index] == bestScore]
            # Pick randomly among the best
            chosenIndex = random.choice(bestIndices)

            return bestScore, chosenIndex

        else:
            bestScore = min(scores)

            return bestScore, 0


    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing
          minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        bestScore, chosenIndex = self.getActionHelper(gameState, 0, self.depth)

        # Collect legal moves
        legalMoves = gameState.getLegalActions()

        return legalMoves[chosenIndex]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getActionHelper(self, gameState, agentIndex, depth, alpha, beta):
        if (depth == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), 0

        # Collect legal moves
        legalMoves = gameState.getLegalActions(agentIndex)\

        # Max
        if agentIndex == 0:
            bestScore= -float('inf')
            chosenIndex = 0

            for action in legalMoves:
                state = gameState.generateSuccessor(agentIndex, action)
                score = self.getActionHelper(state,
                                             agentIndex + 1,
                                             depth,
                                             alpha,
                                             beta)[0]

                if score > bestScore:
                    bestScore = score
                    chosenIndex = [index for index in range(len(legalMoves)) \
                                   if legalMoves[index] == action][0]

                if bestScore > beta:
                    return bestScore, 0

                alpha = max(alpha, bestScore)

            return bestScore, chosenIndex

        # Min
        else:
            bestScore= float('inf')

            for action in legalMoves:
                state = gameState.generateSuccessor(agentIndex, action)
                if agentIndex < gameState.getNumAgents() - 1:
                    bestScore = min(bestScore,
                                    self.getActionHelper(state,
                                                         agentIndex + 1,
                                                         depth,
                                                         alpha,
                                                         beta)[0])
                else:
                    bestScore = min(bestScore,
                                    self.getActionHelper(state,
                                                         0,
                                                         depth - 1,
                                                         alpha,
                                                         beta)[0])

                if bestScore < alpha:
                    return bestScore, 0

                beta = min(beta, bestScore)

            return bestScore, 0

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and
          self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestScore, chosenIndex = self.getActionHelper(gameState,
                                                      0,
                                                      self.depth,
                                                      -float('inf'),
                                                      float('inf'))

        # Collect legal moves
        legalMoves = gameState.getLegalActions()

        return legalMoves[chosenIndex]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getActionHelper(self, gameState, agentIndex, depth):
        if (depth == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), 0

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(agentIndex)
        states = [gameState.generateSuccessor(agentIndex, action) \
                  for action in legalMoves]

        # Recursively collect scores for every successor state
        if agentIndex < gameState.getNumAgents() - 1:
            scores = [self.getActionHelper(state, agentIndex + 1, depth)[0] \
                      for state in states]
        else:
            scores = [self.getActionHelper(state, 0, depth - 1)[0] \
                      for state in states]

        # Choose best score according to current agent
        if agentIndex == 0:
            bestScore = max(scores)

            bestIndices = [index for index in range(len(scores)) \
                           if scores[index] == bestScore]
            # Pick randomly among the best
            chosenIndex = random.choice(bestIndices)

            return bestScore, chosenIndex

        else:
            expectedScore = 1.0 * sum([score for score in scores]) / len(scores)

            return expectedScore, 0

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and
          self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from
          their legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestScore, chosenIndex = self.getActionHelper(gameState, 0, self.depth)

        # Collect legal moves
        legalMoves = gameState.getLegalActions()

        return legalMoves[chosenIndex]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Score is higher the less food that is left, and the smaller
                   the distance to the closest food pellet. If a ghost is
                   nearby we run away.
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()

    height, width = currentGameState.getWalls().height,\
                    currentGameState.getWalls().width
    maxPossibleDist = 2 * (height + width)

    foodLeft = len(foodList)

    # If there is no food left we win, so we choose this action regardless
    if foodLeft == 0:
        return 1000 * maxPossibleDist

    # Get the distance to the closest food pellet
    foodDistances = map(lambda xy:
                        abs(position[0] - xy[0]) + abs(position[1] - xy[1]),
                        foodList)
    closestFoodDist = min(foodDistances)

    # Get the distance to the closest ghost
    ghostDistances = map(lambda xy:
                        abs(position[0] - int(xy.getPosition()[0])) + abs(position[1] - int(xy.getPosition()[1])),
                        ghostStates)
    closestGhostDist = min(ghostDistances)
    ghostPosition = ghostStates[0].getPosition()

    # We want to avoid being too close to the ghost
    if closestGhostDist < 3:
        return -100000

    return 460*maxPossibleDist/foodLeft + maxPossibleDist/closestFoodDist

# Abbreviation
better = betterEvaluationFunction
