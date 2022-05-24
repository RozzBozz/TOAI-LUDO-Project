from itertools import chain
from sre_parse import State
from statistics import mean

from cv2 import getStructuringElement
from ludoHelperFunctions import *
from os.path import exists
import math

# States
HOME = 0
GOAL = 1
APPROACHGOAL = 2
DANGER = 3
SAFE = 4
NORMAL = 5
STATES = [HOME,GOAL,APPROACHGOAL,DANGER,SAFE,NORMAL]

# State dictionary
sDict = {
    "[0, 0, 0, 0]": 0,
    "[0, 0, 0, 1]": 1,
    "[0, 0, 0, 2]": 2,
    "[0, 0, 0, 3]": 3,
    "[0, 0, 0, 4]": 4,
    "[0, 0, 0, 5]": 5,
    "[0, 0, 1, 1]": 6,
    "[0, 0, 1, 2]": 7,
    "[0, 0, 1, 3]": 8,
    "[0, 0, 1, 4]": 9,
    "[0, 0, 1, 5]": 10,
    "[0, 0, 2, 2]": 11,
    "[0, 0, 2, 3]": 12,
    "[0, 0, 2, 4]": 13,
    "[0, 0, 2, 5]": 14,
    "[0, 0, 3, 3]": 15,
    "[0, 0, 3, 4]": 16,
    "[0, 0, 3, 5]": 17,
    "[0, 0, 4, 4]": 18,
    "[0, 0, 4, 5]": 19,
    "[0, 0, 5, 5]": 20,
    "[0, 1, 1, 1]": 21,
    "[0, 1, 1, 2]": 22,
    "[0, 1, 1, 3]": 23,
    "[0, 1, 1, 4]": 24,
    "[0, 1, 1, 5]": 25,
    "[0, 1, 2, 2]": 26,
    "[0, 1, 2, 3]": 27,
    "[0, 1, 2, 4]": 28,
    "[0, 1, 2, 5]": 29,
    "[0, 1, 3, 3]": 30,
    "[0, 1, 3, 4]": 31,
    "[0, 1, 3, 5]": 32,
    "[0, 1, 4, 4]": 33,
    "[0, 1, 4, 5]": 34,
    "[0, 1, 5, 5]": 35,
    "[0, 2, 2, 2]": 36,
    "[0, 2, 2, 3]": 37,
    "[0, 2, 2, 4]": 38,
    "[0, 2, 2, 5]": 39,
    "[0, 2, 3, 3]": 40,
    "[0, 2, 3, 4]": 41,
    "[0, 2, 3, 5]": 42,
    "[0, 2, 4, 4]": 43,
    "[0, 2, 4, 5]": 44,
    "[0, 2, 5, 5]": 45,
    "[0, 3, 3, 3]": 46,
    "[0, 3, 3, 4]": 47,
    "[0, 3, 3, 5]": 48,
    "[0, 3, 4, 4]": 49,
    "[0, 3, 4, 5]": 50,
    "[0, 3, 5, 5]": 51,
    "[0, 4, 4, 4]": 52,
    "[0, 4, 4, 5]": 53,
    "[0, 4, 5, 5]": 54,
    "[0, 5, 5, 5]": 55,
    "[1, 1, 1, 1]": 56,
    "[1, 1, 1, 2]": 57,
    "[1, 1, 1, 3]": 58,
    "[1, 1, 1, 4]": 59,
    "[1, 1, 1, 5]": 60,
    "[1, 1, 2, 2]": 61,
    "[1, 1, 2, 3]": 62,
    "[1, 1, 2, 4]": 63,
    "[1, 1, 2, 5]": 64,
    "[1, 1, 3, 3]": 65,
    "[1, 1, 3, 4]": 66,
    "[1, 1, 3, 5]": 67,
    "[1, 1, 4, 4]": 68,
    "[1, 1, 4, 5]": 69,
    "[1, 1, 5, 5]": 70,
    "[1, 2, 2, 2]": 71,
    "[1, 2, 2, 3]": 72,
    "[1, 2, 2, 4]": 73,
    "[1, 2, 2, 5]": 74,
    "[1, 2, 3, 3]": 75,
    "[1, 2, 3, 4]": 76,
    "[1, 2, 3, 5]": 77,
    "[1, 2, 4, 4]": 78,
    "[1, 2, 4, 5]": 79,
    "[1, 2, 5, 5]": 80,
    "[1, 3, 3, 3]": 81,
    "[1, 3, 3, 4]": 82,
    "[1, 3, 3, 5]": 83,
    "[1, 3, 4, 4]": 84,
    "[1, 3, 4, 5]": 85,
    "[1, 3, 5, 5]": 86,
    "[1, 4, 4, 4]": 87,
    "[1, 4, 4, 5]": 88,
    "[1, 4, 5, 5]": 89,
    "[1, 5, 5, 5]": 90,
    "[2, 2, 2, 2]": 91,
    "[2, 2, 2, 3]": 92,
    "[2, 2, 2, 4]": 93,
    "[2, 2, 2, 5]": 94,
    "[2, 2, 3, 3]": 95,
    "[2, 2, 3, 4]": 96,
    "[2, 2, 3, 5]": 97,
    "[2, 2, 4, 4]": 98,
    "[2, 2, 4, 5]": 99,
    "[2, 2, 5, 5]": 100,
    "[2, 3, 3, 3]": 101,
    "[2, 3, 3, 4]": 102,
    "[2, 3, 3, 5]": 103,
    "[2, 3, 4, 4]": 104,
    "[2, 3, 4, 5]": 105,
    "[2, 3, 5, 5]": 106,
    "[2, 4, 4, 4]": 107,
    "[2, 4, 4, 5]": 108,
    "[2, 4, 5, 5]": 109,
    "[2, 5, 5, 5]": 110,
    "[3, 3, 3, 3]": 111,
    "[3, 3, 3, 4]": 112,
    "[3, 3, 3, 5]": 113,
    "[3, 3, 4, 4]": 114,
    "[3, 3, 4, 5]": 115,
    "[3, 3, 5, 5]": 116,
    "[3, 4, 4, 4]": 117,
    "[3, 4, 4, 5]": 118,
    "[3, 4, 5, 5]": 119,
    "[3, 5, 5, 5]": 120,
    "[4, 4, 4, 4]": 121,
    "[4, 4, 4, 5]": 122,
    "[4, 4, 5, 5]": 123,
    "[4, 5, 5, 5]": 124,
    "[5, 5, 5, 5]": 125
}

# Act"ions
MOVEOUT = 0
MOVESAFE = 1
MOVESTAR = 2
MOVEHOME = 3
MOVEATTACK = 4
MOVESUICIDE = 5
MOVE = 6
STAY = 7 # Only valid if no other actions are avaliable
ACTIONS = [MOVEOUT,MOVESAFE,MOVESTAR,MOVEHOME,MOVEATTACK,MOVESUICIDE,MOVE,STAY]

# Rewards

class AI:

    def reset(self):
        self.firstPass = True
        self.deltaQSum = 0

    def __init__(self, QTableFilePath, alpha=0.5, gamma=0.9, epsilon=0, epsilonDecay = 0.02):
        """
        QTableFilePath: full path of the Q-table
        alpha: Desired alpha value
        gamma: Desired gamma value
        epsilon: Desired epsilon value
        newQTable: If True, allocates a new Q-table instead of using the on loaded by default, or passed in QTableFilePath
        """
        # Attempt to load Q-table
        if not exists(QTableFilePath):
            self.startedFromScratch = True
            numberOfStates = int(math.factorial(4 + len(STATES) - 1) / (math.factorial(4) * math.factorial(len(STATES)-1)))
            self.QTable = np.zeros((numberOfStates, len(ACTIONS)))
        else:
            self.startedFromScratch = False
            self.QTable = np.load(QTableFilePath)
        
        self.data = []
        self.winRates = []
        self.deltaQSum = 0
        self.deltaQSums = []
        # Tells onePass, that the AI has just been initialized
        self.firstPass = False
        # Define the initial state
        self.reset()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilonDecay = epsilonDecay
        self.numberOfGamesPlayed = 0
        self.numberOfWins = 0
        self.curState = []
        self.nextState = []
        self.action = 0
        
    def onePass(self, diceRoll, pieces, enemyPieces, shouldLearn = False):
        """
        diceRoll: Value of the dice rolled. Use diceroll of game observation
        pieces: Indecies of the pieces of the of the player
        enemyPieces: Indecies of the pieces of the enemy players
        shouldLearn: If true, the AI learns
        """ 
        if not self.firstPass:
            # Estimate the reward for being in this state
            self.nextState = self.getState(pieces,enemyPieces)
            if shouldLearn:
                self.calculateReward()
                # Update the Q-value of the current state
                self.updateQValue()
            # Start by updating the state of the AI 
        self.firstPass = False
        # Select an action 
        self.curState = self.getState(pieces,enemyPieces)  
        self.selectAction(diceRoll, pieces, enemyPieces)
        return self.getPieceToMove()

    def decayEpsilon(self, decay):
        """
        Decays the epsilon-value of the AI. (epsilon = epsilon * (100 - decay))
        decay (int) decay in percentage
        """
        self.epsilon = self.epsilon * (1 - decay/100)

    def addWin(self):
        self.numberOfWins += 1

    def addGamePlayed(self):
        self.numberOfGamesPlayed += 1

    def addCurWinRate(self):
        self.winRates.append(self.getCurWinRate())

    def getCurWinRate(self):
        return self.getNumberOfGamesWon() / self.getNumberOfGamesPlayed() * 100

    def getCurState(self):
        return self.curState

    def getNextState(self):
        return self.nextState

    def getState(self,pieces,enemyPieces):
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
            elif isSafe(piece,otherPieces,enemyPieces):
                newStates.append(SAFE)

            # STATE NORMAL
            # No new state
            else:
                newStates.append(NORMAL)
        return newStates

    def getQValueIndex(self,state,action):
        # Use the dictionary when indecing the states
        stateSorted = state.copy()
        stateSorted.sort()
        rowIndex = sDict[str(stateSorted)]
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

        actions = self.getAvaliableActions(pieces,diceRoll,enemyPieces)
        #print("Got actions:", actions)
        # Get the unique actions avaliable.
        uniqueActions = list(set(chain(*actions)))
        # If the list is empty, set the piece to -1 (the piece the game needs to stay) and the index to the STAY action
        if len(uniqueActions) == 0:
            self.action = 7
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
            # THIS SHOULD BE ALTERED TO DEPEND ON THE STATE

            # Find out which pieces can be moved with the chosen action
            avaliablePieces = []
            for index, actionList in enumerate(actions):
                if chosenAction in actionList:
                    avaliablePieces.append(index)

            # If more than one piece matches the chosen action, choose one based on the order of its state
            if len(avaliablePieces) > 1:
                maxSeverity = 7
                for piece in avaliablePieces:
                    if self.curState[piece] == DANGER:
                        curSeverity = 1
                    elif self.curState[piece] == HOME:
                        curSeverity  = 2
                    elif self.curState[piece] == NORMAL:
                        curSeverity = 3
                    elif self.curState[piece] == SAFE:
                        curSeverity = 4
                    elif self.curState[piece] == APPROACHGOAL:
                        curSeverity = 5
                    else: # GOAL
                        curSeverity = 6
                    if curSeverity < maxSeverity:
                        maxSeverity = curSeverity
                        chosenPiece = piece
                    # A piece an't have higher severity than when it is in danger, so break out
                    if maxSeverity == 1:
                        break
                    # No selection for goal, doesn't have any valid actions
            # Pick the only piece corresponding to the action
            else:
                chosenPiece = avaliablePieces[0]
            self.action = chosenAction
            self.pieceToMove = chosenPiece

    def getPieceToMove(self):
        # Get the index of the piece that was chosen by the AI to move during the last call to select action
        return self.pieceToMove

    def calculateReward(self):
        # Calculate reward
        reward = 0
        # Is based on the action chosen
        if self.action == MOVESAFE:
            reward += 1
        elif self.action == MOVESTAR:
            reward += 0.5
        elif self.action == MOVEHOME:
            reward += 0.5
        elif self.action == MOVEATTACK:
            reward += 0.25
        elif self.action == MOVESUICIDE:
            reward -= 1
        elif self.action == MOVE or self.action == STAY:
            reward += 0
        elif self.action == MOVEOUT:
            reward += 1
        # And the next state
        # If the chosen piece is minus one, the reward is zero, since it didn't really choose it
        if self.pieceToMove == -1:
            reward += 0
        else:
            if self.nextState[self.pieceToMove] == HOME:
                reward -= 0.5
            elif self.nextState[self.pieceToMove] == GOAL:
                reward += 0.5
            elif self.nextState[self.pieceToMove] == APPROACHGOAL:
                reward += 1
            elif self.nextState[self.pieceToMove] == DANGER:
                reward -= 0.5
            elif self.nextState[self.pieceToMove] == SAFE:
                reward += 1
            elif self.nextState[self.pieceToMove] == NORMAL:
                reward += 0.75
        
        self.reward = reward

    def updateQValue(self):
        oldQVal = self.getQValue(self.curState,self.action)
        # Find the best action for the new state
        maxQval = 0
        possibleActions = self.getPossibleActions(self.nextState)
        for action in possibleActions:
            if action == STAY:
                continue
            curQVal = self.getQValue(self.nextState,action)
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
        self.setQValue(oldQVal + deltaQVal, self.curState, self.action)        

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
        percentZeroQTable = ((self.getRealQTableSize()-nonZero)/self.getRealQTableSize())*100
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
        self.writeToTXTFile(filename,self.deltaQSums,"Delta Qs")
    
    def saveWinRates(self, filename="winRates.txt"):
        self.writeToTXTFile(filename,self.winRates,"Winrates [%]")

    def addCurDeltaQSum(self):
        self.deltaQSums.append(self.deltaQSum)

    def getPossibleActions(self, states):
        """
        For each state in the passed state, determine which states actions can actually be chosen from
        """
        possibleActions = []
        for state in states:
            if state == HOME:
                possibleActions.append([MOVEOUT,MOVESAFE,MOVEATTACK])
            elif state == GOAL:
                possibleActions.append([])
            elif state == APPROACHGOAL:
                possibleActions.append([MOVEHOME, MOVE])
            # State is DANGER, SAFE or NORMAL
            else:
                possibleActions.append([MOVESAFE,MOVESTAR,MOVEHOME,MOVEATTACK,MOVESUICIDE,MOVE])
        # Only return unique actions
        uniqueActions = list(set(chain(*possibleActions)))
        # If list contains only state HOME and/or state GOAL, it can also perform action STAY
        if (HOME in uniqueActions or GOAL in uniqueActions) and APPROACHGOAL not in uniqueActions and DANGER not in uniqueActions and SAFE not in uniqueActions and MOVEOUT not in uniqueActions:
            uniqueActions.append[STAY]
        return uniqueActions

    def getAvaliableActions(self, pieces, diceRoll, enemyPieces):
        """
        Returns avaliable actions for all pieces in list of lists. All pieces will have zero or more actions
        """
        avaliableActions = [[],[],[],[]]
        for index,piece in enumerate(pieces):
            otherPieces = np.delete(pieces,index)

            # MOVEOUT
            # If a six is rolled, the piece can move out from home
            if canMoveOut(piece,diceRoll):
                avaliableActions[index].append(MOVEOUT)
        
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

    def getRealQTableSize(self):
        qTableSize = 0
        for key in sDict:
            # Omit square brackets
            slice = key[1:-1]
            # Squeeze string, so vals are next to each pther
            slice = slice.replace(", ","")
            # Make it to list
            state = [int(x) for x in slice]
            qTableSize += len(self.getPossibleActions(state))
        return qTableSize