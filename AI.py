from sre_parse import State
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
ACTIONS = [MOVESAFE,MOVESTAR,MOVEHOME,MOVEATTACK,MOVESUICIDE,MOVE]

# Rewards

class AI:

    def reset(self,):
        self.prevState = []
        self.action = []
        self.curState = [HOME,HOME,HOME,HOME]
        self.reward = 0

    def __init__(self,QTableFileName,alpha=0.5,gamma=0.9, epsilon=0.1, startFromScratch = False):
        # Specifies if the AI started learning from scratch
        self.startedFromScratch = startFromScratch
        # Attempt to load Q-table
        if startFromScratch or not exists(QTableFileName):
            numberOfStates = int(math.factorial(4 + len(STATES) - 1) / (math.factorial(4) * math.factorial(len(STATES)-1)))
            self.QTable = np.zeros((numberOfStates, len(ACTIONS)*4+1))
        else:
            self.QTable = np.load(QTableFileName)
        self.data = []
        self.winRates = []   
        # Define the initial state
        self.reset()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.numberOfGamesPlayed = 0
        self.numberOfWins = 0

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
        columnIndex = action[0] + action[1] + 5 * action[0]
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

        # Check if there are any valid actions, otherwise set to [-1 24]
        lenPieceActions = []
        for actionList in actions:
            lenPieceActions.append(len(actionList))
        if sum(lenPieceActions) == 0:
            self.action = [-1, 24]
        else:
            # Remove all pieces, who don't have any actions
            avaliablePieces = []
            for index, _ in enumerate(lenPieceActions):
                if lenPieceActions[index] != 0:
                    avaliablePieces.append(index)

            randomActionChance = np.random.randint(0, 100) # (0 to 99)
            #print("Random Action selection, rolled", randomActionChance)
            if randomActionChance < self.epsilon:
                # Select one of the avaliable pieces at random
                #print("AI chose a random action!")
                #print("Avaliable Pieces", avaliablePieces)
                if len(avaliablePieces) == 1:
                    pieceIndex = avaliablePieces[0]
                    #print("Only one valid piece! Chose number", pieceIndex)
                    if len(actions[pieceIndex]) == 1:
                        self.action = [pieceIndex,actions[pieceIndex][0]]
                        #print("And only one valid action! Chose action", actions[pieceIndex][0])
                    else:
                        actionIndex = np.random.randint(0,len(actions[pieceIndex]))
                        self.action = [pieceIndex,actions[pieceIndex][actionIndex]]
                        #print("But more than one action! Chose action", actions[pieceIndex][actionIndex])
                else:
                    pieceIndex = np.random.randint(0,len(avaliablePieces))
                    #print("More than one valid piece! Chose number", avaliablePieces[pieceIndex])
                    if len(actions[avaliablePieces[pieceIndex]]) == 1:
                        self.action = [avaliablePieces[pieceIndex],actions[avaliablePieces[pieceIndex]][0]]
                        #print("But only one valid action! Chose action", actions[avaliablePieces[pieceIndex]][0])
                    else:
                        actionIndex = np.random.randint(0,len(actions[avaliablePieces[pieceIndex]]))
                        self.action = [avaliablePieces[pieceIndex],actions[avaliablePieces[pieceIndex]][actionIndex]]
                        #print("And more than one action! Chose action", actions[pieceIndex][actionIndex])
            else:
                #print("AI is choosing max action!")
                #print("From pieces", avaliablePieces)
                bestPieceNumber, bestQVal, bestAction = 0, 0, 0
                firstAction = True
                for pieceIndex in avaliablePieces:
                    for action in actions[pieceIndex]:
                        curQVal = self.getQValue(self.curState,[pieceIndex,action])
                        # If this is the first action that's being checked, set that as the benchmark to beat
                        if firstAction:
                            bestQVal = curQVal
                            bestPieceNumber = pieceIndex
                            bestAction = action
                            firstAction = False
                            continue
                        # If this Q-value is better than the current, update it                       
                        if curQVal > bestQVal:
                            bestQVal = curQVal
                            bestPieceNumber = pieceIndex
                            bestAction = action
                #print("The max action chosen was", [bestPieceNumber,bestAction])
                #print("With Q-value", bestQVal)
                self.action = [bestPieceNumber,bestAction]

    def getPieceIndexMove(self):
        # Get the index of the piece that was chosen by the AI to move during the last call to select action
        return self.action[0]

    def calculateReward(self,round,pieces):
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
        
        # Decrease reward base on round timer
        #reward -= round * 0.005
        #print("Calculated reward", reward)
        self.reward = reward

    def updateQValue(self):
        if self.action[1] == 24: # No valid action, AI must stay
            oldQVal = self.getQValue(self.prevState,[0,24])
        else:
            oldQVal = self.getQValue(self.prevState,self.action)
        # Find the best action for the new state
        maxQval = 0
        for i in range (0,4): # Always four pieces
            for j in range(0,len(ACTIONS)): # Always len(ACTIONS)+1 amount of actions, since the last action is stay, if no other actions are avaliable
                curQVal = self.getQValue(self.curState,[i,j])
                if curQVal > maxQval:
                    maxQval = curQVal
        # Also check the stay Q-value
        stayQVal = self.getQValue(self.curState,[0,24])
        if stayQVal > curQVal:
            maxQval = stayQVal
        #print("Old Q value",oldQVal)
        #print("abs of that",abs(oldQVal))
        #print("Max Q value", maxQval)
        #print("self reward", self.reward)
        deltaQVal = self.alpha * (self.reward + self.gamma * maxQval - oldQVal)
        #print("New Q-value", newVal)
        # If the current action was to stay, make sure to call the update correctly
        if self.action[1] == 24:
            self.setQValue(oldQVal + deltaQVal, self.prevState, [0,24])  
        else:
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
        percentZeroQTable = np.count_nonzero(self.QTable==0)/(self.QTable.shape[0]*self.QTable.shape[1])*100
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
    
    def updateWinRates(self):
        self.winRates.append(self.getCurWinRate())

    def saveWinRates(self, filename="winRates.txt"):
        self.writeToTXTFile(filename,self.winRates,"Winrates [%]")

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