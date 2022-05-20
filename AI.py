from ludopy.player import get_enemy_at_pos
from ludoHelperFunctions import *

# States
HOME = 0
GOAL = 1
APPROACHGOAL = 2
DANGER = 3
SAFE = 4
STATES = [HOME,GOAL,APPROACHGOAL,DANGER,SAFE]

# Actions
MOVEOUT = 0
MOVEATTACK = 1
MOVESTAR = 2
MOVESAFE = 3
MOVEHOME = 4
MOVE = 5
ACTIONS = [MOVEOUT,MOVEATTACK,MOVESTAR,MOVESAFE,MOVEHOME,MOVE]

# Rewards


class AI:

    def __init__(self,filename,alpha=0.5,gamma=0.9, epsilon=0.1):
        # Load Q-table file from path
        # If it doesn't exist, allocate a new one
        #self.QTable =
        # Define the initial state
        self.prevState = []
        self.curState = [HOME,HOME,HOME,HOME]
        self.numberOfGamesPlayed = 0
        self.numberOfWins = 0
        self.winrate = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def getState(self):
        return self.curState

    def setState(self,playerPieces,enemyPiecesLists):
        # Update state based on current board
        newStates = []
        for piece in playerPieces:

            # STATE HOME
            # Checks if the piece is home
            if isAtHome(piece):
                newStates.append(HOME)

            # STATE GOAL
            # Checks if the piece is in goal
            elif isInGoal(piece):
                newStates.append(GOAL)
                
            # STATE APPROACHHOME
            # Checks if the piece is in the safe zone before home
            elif isInApproachToGoal(piece):
                newStates.append(APPROACHGOAL)

            # STATE DANGER
            # Checks if the piece is in danger
            elif isInDanger(piece, enemyPiecesLists):
                newStates.append(DANGER)

            # STATE SAFE
            # If no of the other states apply, the state of the current piece is safe
            else:
                newStates.append(SAFE)
        # Update the states
        self.prevState = self.curState
        self.curState = newStates

    def selectAction(self,diceRoll,pieces,state):
        # Select an action based on the epsilon greedy equation
        # Depends on the dice roll
        # List of avaliable actions for all pieces
        avaliableActions = []
        for index,piece in enumerate(pieces):
            actions = []
            # MOVEOUT
            # If a six is rolled, the piece can move out from the home-field
            if piece == 0 and diceRoll == 6:
                avaliableActions.append(MOVEOUT)
                continue
        
            # MOVEATTACK
            # If the piece can go to the same space as an enemy piece that is not safe

            # MOVESTAR
            # If the piece can go to a space containing a star
            if diceRoll == distToNearestStar(piece):
                avaliableActions.append(MOVESTAR)

            # MOVESAFE
            # If the piece can move to a space with another piece, in the goal zone, 

            # MOVE
            # A piece can always move, unless it is home
            avaliableActions.append(MOVE)
            actions.extend(avaliableActions)
        
        # Select a random value between 0 and 100, if smaller than epsilon, choose a random action
        # Else, choose action with largest Q value
        # Return the action

    def calculateReward(self,state,round):
        # Calculate and return reward
        pass

    def updateQTable(self,state,action,reward):
        pass

    # Don't think i should actually make this function, otherwise the game will have to be passed as well
    def performOnePass(self):
        # State, action, reward, state, action
        # Get current state of AI-player, save it for update
        # Select an action
        # Grab Q-value from table
        # Perform action, transistion to new state
        # Get reward
        # Update Q-table
        pass

    def saveQTable(self,filename):
        # Save to class Q-table to a file
        pass