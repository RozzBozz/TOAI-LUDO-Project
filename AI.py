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

    def reset(self, resetQTable = False):
        # If resetQTable is True, initialize a new Q-table        
        self.prevState = []
        self.curState = [HOME,HOME,HOME,HOME]

    def __init__(self,filename="",alpha=0.5,gamma=0.9, epsilon=0.1):
        # If filename is given, attempt to load it
        # If it exists, use that
        # Else, initialize empty Q-table
        # If no filename is given, initialize an empty Q-table
        # Load Q-table file from path
        # If it doesn't exist, allocate a new one
        #self.QTable =
        # Define the initial state
        self.resetState()
        self.numberOfGamesPlayed = 0
        self.numberOfWins = 0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def addWin(self):
        self.numberOfWins = self.numberOfWins + 1

    def addGamePlayed(self):
        self.numberOfGamesPlayed = self.numberOfGamesPlayed + 1

    def getWinRate(self):
        return self.numberOfWins / self.numberOfGamesPlayed

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
        # Returns the index of the selected piece
        # Get avaliable actions
        actions = getAvaliableActions(pieces,diceRoll,enemyPieces)
        
        # Check if there are any valid actions, otherwise return -1
        if sum(actionList[0]) + sum(actionList[1]) + sum(actionList[2]) + sum(actionList[3]) == 0:
            return -1

        randomActionChance = np.random.randint(0, 100) # (0 to 99)
        if randomActionChance < self.epsilon:
            # Perform random action
            print("Choosing random action!")
            pieceNumber = np.random.randInt(0,4) # (0 to 3)
            return pieceNumber
        else:
            print("Choosing max action!")
            # In the Q-table, the row corresponds to the state, and the 
            bestPieceNumber, bestQVal = 0
            for pieceIndex,actionList in enumerate(actions):
                for action in actionList:
                    # Get Q-value of current action/state. Action index in Q-table must be action*pieceIndex
                    # State index is the index of the current state, must be self.curState[0] + self.curState[1] * 5 + seld.curState[2] * 25 + self.curState[3] * 125
                    curQVal = 0 # Input actual Q-value
                    if curQVal > bestQVal:
                        bestQVal = curQVal
                        bestPieceNumber = pieceIndex
            return bestPieceNumber

    def calculateReward(self,state,round):
        # Calculate and return reward
        pass

    def updateQTable(self,state,action,reward):
        pass

    def saveQTable(self,filename):
        # Save to class Q-table to a file
        pass

    def saveWinRate(self,filename):
        #TODO Implement appending win-rate to file
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