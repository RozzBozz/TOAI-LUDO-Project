from lib2to3.refactor import MultiprocessingUnsupported
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
#MOVEOUT = 0
MOVESAFE = 0
MOVESTAR = 1
MOVEHOME = 2
MOVEATTACK = 3
MOVESUICIDE = 4
MOVE = 5
ACTIONS = [MOVESAFE,MOVESTAR,MOVEHOME,MOVEATTACK,MOVESUICIDE,MOVE]

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

    def updateState(self,pieces,enemyPieces):
        # Update state based on current board
        newStates = []
        for index,piece in enumerate(pieces):
            otherPieces = np.delete(pieces,index)
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
            elif isInDanger(piece, otherPieces, enemyPieces):
                newStates.append(DANGER)

            # STATE SAFE
            # If no of the other states apply, the state of the current piece is safe
            else:
                newStates.append(SAFE)
        # Update the states
        self.prevState = self.curState
        self.curState = newStates

    def selectAction(self,diceRoll,pieces,enemyPieces):
        # Select an action based on the epsilon greedy equation

        # Maybe wrap all of this in a nice class in the helper functions file?
        # This way it can be used when creating semi-random players
        # Save it for later

        actions = getAvaliableActions(pieces,diceRoll,enemyPieces)
        
        # Select a random value between 0 and 100, if smaller than epsilon, choose a random action
        # Else, choose action with largest Q value
        # Return the action

    def calculateReward(self,state,round):
        # Calculate and return reward
        pass

    def updateQTable(self,state,action,reward):
        pass

    def saveQTable(self,filename):
        # Save to class Q-table to a file
        pass

def getAvaliableActions(pieces, diceRoll, enemyPieces):
    """
    Returns avaliable actions for all pieces in list of lists. All pieces will have zero or more actions
    """
    avaliableActions = [[],[],[],[]]
    for index,piece in enumerate(pieces):
        otherPieces = np.delete(pieces,index)

        # MOVEOUT
        # If a six is rolled, the piece can move out from home
        #if canMoveOut(piece,diceRoll):
        #    avaliableActions[index].append(MOVEOUT)
        #    continue
    
        # MOVESAFE
        # If the piece can move to a space with another piece, into the goal zone or to another friendly piece
        if canMoveSafe(piece, otherPieces, diceRoll, enemyPieces):
            avaliableActions[index].append(MOVESAFE)

        # MOVESTAR
        # If the piece can go to a space containing a star, where there aren't two enemy pieces
        if canMoveStar(piece,diceRoll,enemyPieces):
            avaliableActions[index].append(MOVESTAR)

        # MOVEHOME
        # If the piece can move
        if canMoveHome(piece,diceRoll,enemyPieces):
            avaliableActions[index].append(MOVEHOME)

        # MOVEATTACK
        # If the piece can go to the same space as an enemy piece that is not safe
        if canAttack(piece,diceRoll,enemyPieces):
            avaliableActions[index].append(MOVEATTACK)

        # MOVESUICIDE
        # If the piece can move to a tile that results in it being knocked home
        if canSuicide(piece,diceRoll,enemyPieces):
            avaliableActions[index].append(MOVESUICIDE)

        # MOVE
        # A piece can always move if no other move are avaliable, and it is not at home or in goal
        if canMove(piece) and len(avaliableActions[index]) == 0:
            avaliableActions[index].append(MOVE)

    return avaliableActions