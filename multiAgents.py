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
import random, util, sys

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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if newScaredTimes[0] != 0:
          gScore = 2 * min(newScaredTimes[0], 6)
        else:
          gPoss = [gState.getPosition() for gState in newGhostStates]
          gScore = 2 * min(min([manhattanDistance(newPos, gPos) for gPos in gPoss]), 6)
        fDist = [manhattanDistance(newPos, fPos) for fPos in newFood.asList()]
        if len(fDist) == 0:
          fDist = [0]
        return gScore - min(fDist) - 10*len(newFood.asList()) + successorGameState.getScore() 

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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        solver = MiniMaxSolver(self)
        return solver.solve(gameState)

class MiniMaxSolver:
    def __init__(self, agent, alpha_beta = False, expectimax = False):
        self.agent = agent
        self.alpha_beta = alpha_beta
        self.expectimax = expectimax

    def solve(self, state):
        actions = state.getLegalActions(0)
        nodeVals = []
        alpha = -sys.maxint
        beta = sys.maxint
        for action in actions:
          newState = state.generateSuccessor(0, action)
          val = self.getNodeVal(newState, 1, self.agent.depth-1, alpha, beta)
          nodeVals.append(val)
          alpha = max(alpha, val)
        maxNodeVal = max(nodeVals)
        return actions[nodeVals.index(maxNodeVal)]

    def getNodeVal(self, state, agent, depth, alpha = -sys.maxint, beta = sys.maxint):
        if agent == state.getNumAgents():
          # nex ply or evaluate
          if depth == 0:
            return self.agent.evaluationFunction(state)
          else:
            depth -= 1
            agent = 0
        if state.isWin() or state.isLose():
          return self.agent.evaluationFunction(state)
        actions = state.getLegalActions(agent)
        subNodeVals = []
        if self.alpha_beta:
          if agent == 0:
            vi = alpha
          else:
            vi = beta
        for action in actions:
          newState = state.generateSuccessor(agent, action)
          val = self.getNodeVal(newState, agent+1, depth, alpha, beta)
          if self.alpha_beta:
            if agent == 0:
              vi = max(vi, val)
              if vi > beta:
                return vi
              alpha = max(alpha, vi)
            else:
              vi = min(vi, val)
              if vi < alpha:
                return vi
              beta = min(beta, vi)
          subNodeVals.append(val)
        if agent == 0:
          return max(subNodeVals)
        else:
          if self.expectimax:
            return float(sum(subNodeVals))/len(subNodeVals)
          else:
            return min(subNodeVals)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        solver = MiniMaxSolver(self, True)
        return solver.solve(gameState)

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
        solver = MiniMaxSolver(self, False, True)
        return solver.solve(gameState)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <evaluate current state using linear combination of several game features>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    if newScaredTimes[0] != 0:
      gScore = 2 * min(newScaredTimes[0], 6)
    else:
      gPoss = [gState.getPosition() for gState in newGhostStates]
      gScore = 2 * min(min([manhattanDistance(newPos, gPos) for gPos in gPoss]), 6)
    fDist = [manhattanDistance(newPos, fPos) for fPos in newFood.asList()]
    if len(fDist) == 0:
      fDist = [0]
    return gScore - min(fDist) - 10*len(newFood.asList()) + currentGameState.getScore() 

# Abbreviation
better = betterEvaluationFunction

