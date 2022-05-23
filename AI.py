from itertools import chain
from sre_parse import State
from statistics import mean
from ludoHelperFunctions import *
from os.path import exists
import math

# States
HOME = 0
GOAL = 1
APPROACHGOAL = 2
DANGER = 3
SAFE = 4
STATES = [HOME,GOAL,APPROACHGOAL,DANGER,SAFE]

# State dictionary
sDict = {
    "[0, 0, 0, 0]": 0,
    "[0, 0, 0, 1]": 1,
    "[0, 0, 0, 2]": 2,
    "[0, 0, 0, 3]": 3,
    "[0, 0, 0, 4]": 4,
    "[0, 0, 1, 1]": 5,
    "[0, 0, 1, 2]": 6,
    "[0, 0, 1, 3]": 7,
    "[0, 0, 1, 4]": 8,
    "[0, 0, 2, 2]": 9,
    "[0, 0, 2, 3]": 10,
    "[0, 0, 2, 4]": 11,
    "[0, 0, 3, 3]": 12,
    "[0, 0, 3, 4]": 13,
    "[0, 0, 4, 4]": 14,
    "[0, 1, 1, 1]": 15,
    "[0, 1, 1, 2]": 16,
    "[0, 1, 1, 3]": 17,
    "[0, 1, 1, 4]": 18,
    "[0, 1, 2, 2]": 19,
    "[0, 1, 2, 3]": 20,
    "[0, 1, 2, 4]": 21,
    "[0, 1, 3, 3]": 22,
    "[0, 1, 3, 4]": 23,
    "[0, 1, 4, 4]": 24,
    "[0, 2, 2, 2]": 25,
    "[0, 2, 2, 3]": 26,
    "[0, 2, 2, 4]": 27,
    "[0, 2, 3, 3]": 28,
    "[0, 2, 3, 4]": 29,
    "[0, 2, 4, 4]": 30,
    "[0, 3, 3, 3]": 31,
    "[0, 3, 3, 4]": 32,
    "[0, 3, 4, 4]": 33,
    "[0, 4, 4, 4]": 34,
    "[1, 1, 1, 1]": 35,
    "[1, 1, 1, 2]": 36,
    "[1, 1, 1, 3]": 37,
    "[1, 1, 1, 4]": 38,
    "[1, 1, 2, 2]": 39,
    "[1, 1, 2, 3]": 40,
    "[1, 1, 2, 4]": 41,
    "[1, 1, 3, 3]": 42,
    "[1, 1, 3, 4]": 43,
    "[1, 1, 4, 4]": 44,
    "[1, 2, 2, 2]": 45,
    "[1, 2, 2, 3]": 46,
    "[1, 2, 2, 4]": 47,
    "[1, 2, 3, 3]": 48,
    "[1, 2, 3, 4]": 49,
    "[1, 2, 4, 4]": 50,
    "[1, 3, 3, 3]": 51,
    "[1, 3, 3, 4]": 52,
    "[1, 3, 4, 4]": 53,
    "[1, 4, 4, 4]": 54,
    "[2, 2, 2, 2]": 55,
    "[2, 2, 2, 3]": 56,
    "[2, 2, 2, 4]": 57,
    "[2, 2, 3, 3]": 58,
    "[2, 2, 3, 4]": 59,
    "[2, 2, 4, 4]": 60,
    "[2, 3, 3, 3]": 61,
    "[2, 3, 3, 4]": 62,
    "[2, 3, 4, 4]": 63,
    "[2, 4, 4, 4]": 64,
    "[3, 3, 3, 3]": 65,
    "[3, 3, 3, 4]": 66,
    "[3, 3, 4, 4]": 67,
    "[3, 4, 4, 4]": 68,
    "[4, 4, 4, 4]": 69
}

# Actions
#MOVEOUT = 0
MOVESAFE = 0
MOVESTAR = 1
MOVEHOME = 2
MOVEATTACK = 3
MOVESUICIDE = 4
MOVE = 5
STAY = 6 # Only valid if no other actions are avaliable
ACTIONS = [MOVESAFE,MOVESTAR,MOVEHOME,MOVEATTACK,MOVESUICIDE,MOVE,STAY]

# Rewards

class AI:

    def reset(self,):
        self.prevState = []
        self.action = []
        self.curState = [HOME,HOME,HOME,HOME]
        self.reward = 0
        self.itrNumber = 0

    def __init__(self,QTableFilePath,alpha=0.5,gamma=0.9, epsilon=0.1, newQTable = False):
        """
        QTableFilePath: full path of the Q-table
        alpha: Desired alpha value
        gamma: Desired gamma value
        epsilon: Desired epsilon value
        newQTable: If True, allocates a new Q-table instead of using the on loaded by default, or passed in QTableFilePath
        """
        # Specifies if the AI started learning from scratch
        self.startedFromScratch = newQTable
        # Attempt to load Q-table
        if newQTable or not exists(QTableFilePath):
            numberOfStates = int(math.factorial(4 + len(STATES) - 1) / (math.factorial(4) * math.factorial(len(STATES)-1)))
            self.QTable = np.zeros((numberOfStates, len(ACTIONS)))
        else:
            self.QTable = np.load(QTableFilePath)
        self.data = []
        self.winRates = []
        self.deltaQSum = 0   
        # Define the initial state
        self.reset()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.numberOfGamesPlayed = 0
        self.numberOfWins = 0

    def onePass(self, diceRoll, pieces, enemyPieces, shouldLearn = False):
        """
        diceRoll: Value of the dice rolled. Use diceroll of game observation
        pieces: Indecies of the pieces of the of the player
        enemyPieces: Indecies of the pieces of the enemy players
        shouldLearn: If true, the AI updates the value of the Q-table for each move
        """ 
        if self.itrNumber != 0:
            # Start by updating the state of the AI
            self.updateState(pieces,enemyPieces)
            # Estimate the reward for being in this state
            if shouldLearn:
                self.calculateReward(pieces)
                # Update the Q-value of the previous state
                self.updateQValue()
        # Select an action   
        self.selectAction(diceRoll, pieces, enemyPieces)
        self.itrNumber += 1
        return self.getPieceToMove()

    def addWin(self):
        self.numberOfWins += 1

    def addGamePlayed(self):
        self.numberOfGamesPlayed += 1

    def getCurWinRate(self):
        return self.numberOfWins / self.numberOfGamesPlayed * 100

    def getCurState(self):
        return self.curState

    def getPrevState(self):
        return self.prevState

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
        
        #print("Going from state", self.curState, "to state", newStates)
        self.prevState = self.curState
        # Sort the new states, so that indexing becomes easier
        newStates.sort()
        self.curState = newStates

    def getQValueIndex(self,state,action):
        # Use the dictionary when indecing the states
        rowIndex = sDict[str(state)]
        # Column index in Q-table must be pieceIndex + action + 5 * pieceIndex
        columnIndex = action
        return [rowIndex,columnIndex]
    
    def getQValue(self,state,action):
        index = self.getQValueIndex(state,action)
        return self.QTable[index[0]][index[1]]

    def setQValue(self,value,state,action):
        #print("Setting value", value)
        #print("For state", state)
        #print("And action", action)
        index = self.getQValueIndex(state,action)
        #print("Got index", index)
        self.QTable[index[0],index[1]] = value

    def selectAction(self,diceRoll,pieces,enemyPieces):       
        # Select an action based on the epsilon greedy action selection
        # The action set is a list with two elements, the first being the index of the piece moving, and the second the action chosen

        actions = getAvaliableActions(pieces,diceRoll,enemyPieces)
        #print("Got actions:", actions)
        # Get the unique actions avaliable.
        uniqueActions = list(set(chain(*actions)))
        # If the list is empty, set the piece to -1 (the piece the game needs to stay) and the index to the STAY action
        if len(uniqueActions) == 0:
            self.action = 6
            self.pieceToMove = -1
        else:
            # Select if the choice should be random, or max
            randomActionChance = np.random.randint(0, 100) # (0 to 99)
            #print("Random Action selection, rolled", randomActionChance)
            # Controls which action is chosen.
            # Per default, the chosen actions is the first unique action
            chosenAction = uniqueActions[0]
            chosenPiece = 0
            if randomActionChance < self.epsilon:
                # Choose between one of the unique actions
                randomAction = np.random.randint(0,len(uniqueActions))
                chosenAction = uniqueActions[randomAction]
            else:
                bestQVal = 0
                # Iterate through unique actions, find the largest Q-value
                # This is protected, because the chosenAction is set to the first unique action per default,
                # so even if no better q-value is found, the chosen actions is still valid
                for action in uniqueActions:
                    curQVal = self.getQValue(self.curState, action)
                    if curQVal > bestQVal:
                        bestQVal = curQVal
                        chosenAction = action

            # Choose the piece to which the actions is associated, or the first if there are multiple
            for index, actionList in enumerate(actions):
                if chosenAction in actionList:
                    chosenPiece = index
                    break
            self.action = chosenAction
            self.pieceToMove = chosenPiece

    def getPieceToMove(self):
        # Get the index of the piece that was chosen by the AI to move during the last call to select action
        return self.pieceToMove

    def calculateReward(self,pieces):
        # Calculate and set reward
        reward = 0
        for state in self.curState:
            if state == HOME:
                reward -= 0.5
            elif state == GOAL:
                reward += 1 # 2
            elif state == APPROACHGOAL:
                reward += 1 # 2
            elif state == DANGER:
                reward -= 0.5
            elif state == SAFE:
                reward += 0.5 # 1
        
        # Decrease reward based on distance to goal zone
        for piece in pieces:
            #reward += piece / 39.3 - 0.5
            if piece < 52:
                reward += piece / 216 - 0.25 # max is 0.25, min is 0.01.
        
        self.reward = reward

    def updateQValue(self):
        oldQVal = self.getQValue(self.prevState,self.action)
        # Find the best action for the new state
        maxQval = 0
        possibleActions = getPossibleActions(self.curState)
        for action in possibleActions:
            if action == STAY:
                continue
            curQVal = self.getQValue(self.curState,action)
            if curQVal > maxQval:
                maxQval = curQVal
        #print("Old Q value",oldQVal)
        #print("abs of that",abs(oldQVal))
        #print("Max Q value", maxQval)
        #print("self reward", self.reward)
        deltaQVal = self.alpha * (self.reward + self.gamma * maxQval - oldQVal)
        self.deltaQSum += deltaQVal # Append delta Q val to array to see if it converges
        #print("New Q-value", newVal)
        # If the current action was to stay, make sure to call the update correctly
        self.setQValue(oldQVal + deltaQVal, self.prevState, self.action)        

    def saveQTable(self,filename="QTable.npy"):
        np.save(filename,self.QTable)

    def writeToTXTFile(self,filename,dataList,header):
        # Default write mode is appending
        writeMode = 'a'
        # If the AI started from scratch, overwrite the file
        if self.startedFromScratch:
            writeMode = 'w'
        # Open the file
        file = open(filename, writeMode)
        # Start by writing the header, if overwriting the file
        if writeMode == 'w':
            file.write(header + "\n")
        for index, data in enumerate(dataList):
            # If appending, write a new line to the file
            if index == 0 and writeMode == 'a':
                file.write("\n")
            file.write(str(data) + ",")

    def saveDataFile(self,filename="dataFile.txt"):
        # Win rate
        winRate = self.getCurWinRate()
        # Percent of Q table empty
        nonZero = 0
        for row in self.QTable:
            for column in row:
                if column != 0:
                    nonZero += 1
        percentZeroQTable = ((getRealQTableSize()-nonZero)/getRealQTableSize())*100
        # Max Q value
        maxQ = self.QTable.max()
        # Min Q value
        minQ = self.QTable.min()
        # State for the max Q value
        locationMaxQ = [np.where(self.QTable == np.amax(self.QTable))[0], np.where(self.QTable == np.amax(self.QTable))[1]]
        qMax4Index = int(math.floor(locationMaxQ[0][0] / 125))
        remainder = locationMaxQ[0][0] % 125
        qMax3Index = int(math.floor(remainder / 25))
        remainder = remainder % 25
        qMax2Index = int(math.ceil(remainder / 5))
        remainder = remainder % 5
        qMax1Index = remainder
        qMaxState = [qMax1Index, qMax2Index, qMax3Index, qMax4Index]
        # Piece and action for the max value
        maxPiece = int(math.floor(locationMaxQ[1][0] / 6))
        maxAction = locationMaxQ[1][0] % 6
        # State for the min Q value
        locationMinQ = [np.where(self.QTable == np.amin(self.QTable))[0], np.where(self.QTable == np.amin(self.QTable))[1]]
        qMin4Index = int(math.floor(locationMinQ[0][0] / 125))
        remainder = locationMinQ[0][0] % 125
        qMin3Index = int(math.floor(remainder / 25))
        remainder = remainder % 25
        qMin2Index = int(math.floor(remainder / 5))
        remainder = remainder % 5
        qMin1Index = remainder
        # Piece and action for the min value
        minPiece = int(math.floor(locationMinQ[1][0] / 6))
        minAction = locationMinQ[1][0] % 6
        qMinState = [qMin1Index, qMin2Index, qMin3Index, qMin4Index]
        # Create list with data
        newData = [winRate, percentZeroQTable, maxQ, qMaxState[0], qMaxState[1], qMaxState[2], qMaxState[3], maxPiece, maxAction, minQ, qMinState[0], qMinState[1], qMinState[2], qMinState[3], minPiece, minAction]
        # Write it to file
        self.writeToTXTFile(filename,newData,"Winrate [%], Empty Q Table [%], Max Q, State 1, State 2, State 3, State 4, Piece, Action, Min Q, State 1, State 2, State 3, State 4, Piece, Action")

    def getNumberOfGamesPlayed(self):
        return self.numberOfGamesPlayed

    def getNumberOfGamesWon(self):
        return self.numberOfWins

    def saveDeltaQs(self, filename="deltaQs.txt"):
        self.writeToTXTFile(filename,self.deltaQSum,"Delta Qs")
    
    def saveWinRates(self, filename="winRates.txt"):
        self.writeToTXTFile(filename,self.winRates,"Winrates [%]")

def getPossibleActions( states):
    """
    For each state in the passed state, determine which states can actually be chosen from
    """
    possibleActions = []
    for state in states:
        if state == HOME:
            possibleActions.append([MOVESAFE,MOVEATTACK])
        elif state == GOAL:
            possibleActions.append([])
        elif state == APPROACHGOAL:
            possibleActions.append([MOVESAFE,MOVEHOME])
        elif state == DANGER or state == SAFE:
            possibleActions.append([MOVESAFE,MOVESTAR,MOVEHOME,MOVEATTACK,MOVESUICIDE,MOVE])
    # Only return unique actions
    uniqueActions = list(set(chain(*possibleActions)))
    # If list contains only state HOME and/or state GOAL, it can also perform action STAY
    if (HOME in uniqueActions or GOAL in uniqueActions) and APPROACHGOAL not in uniqueActions and DANGER not in uniqueActions and SAFE not in uniqueActions:
        uniqueActions.append[STAY]
    return uniqueActions

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

def getRealQTableSize():
    qTableSize = 0
    for key in sDict:
        # Omit square brackets
        slice = key[1:-1]
        # Squeeze string, so vals are next to each pther
        slice = slice.replace(", ","")
        # Make it to list
        state = [int(x) for x in slice]
        qTableSize += len(getPossibleActions(state))
    return qTableSize