from ludopy.player import get_enemy_at_pos
from ludoHelperFunctions import *

# States
HOME = 0
GOAL = 1
SAFE = 2
DANGER = 3
NORMAL = 4
STATES = [HOME,GOAL,SAFE,DANGER,NORMAL]

# Actions
MOVEOUT = 0
MOVEATTACK = 1
MOVESTAR = 2
MOVESAFE = 3
MOVE = 4
ACTIONS = [MOVEOUT,MOVEATTACK,MOVESTAR,MOVESAFE,MOVE]

# Rewards


class AI:

    def __init__(self,filename,alpha=0.5,epsilon=0.9):
        # Load Q-table file from path
        # If it doesn't exist, allocate a new one
        #self.QTable =
        # Define the initial state
        self.prevState = []
        self.curState = [HOME,HOME,HOME,HOME]
        self.numberOfGamesPlayed = 0
        self.numberOfWins = 0

    def getState(self):
        return self.curState

    def setState(self,playerPieces,enemyPieces):
        # Update state based on current board
        newStates = []
        for index,piece in enumerate(playerPieces):
            inDanger = False
            otherPieces = playerPieces
            otherPieces.pop(index)

            # STATE HOME
            # If the index of the piece is zero, the piece is home
            if piece == 0:
                newStates.append(HOME)
                continue

            # STATE GOAL
            # If the index of the piece is at the end, the piece is in goal
            if piece == 59:
                newStates.append(GOAL)
                continue

            # STATE SAFE
            # If the piece is at one of globes that is not one of the other player home goals, it is safe
            if piece == 1 or piece == 9 or piece == 22 or piece == 35 or piece == 48:
                newStates.append(SAFE)
                continue
            # If the piece is in the approach to the goal, it is also safe
            if piece >= 53 and piece < 59:
                newStates.append(SAFE)
                continue
            # If the piece is at the same index as one of the other pieces, it is also safe.
            # Doesn't include home or goal indicies
            if piece in otherPieces:
                newStates.append(SAFE)
                continue
            # If the piece is at one of the enemy home globes, and no enemy pieces are home, then it is safe
            # TODO

            # STATE DANGER
            # TODO: A SPECIAL CASE HAS TO MADE IF IT IS STANDING ON A STAR
            # If the piece is range of an enemy piece, then it is in danger
            if piece >= 7:
                for i in range((piece-6),piece):
                    enemiesPresent,_ = get_enemy_at_pos(i,enemyPieces)
                    if enemiesPresent != -1:
                        inDanger = True
                        break
            else:
                for i in range((piece-6),piece):
                    if i <= 0:
                        enemiesPresent,_ = get_enemy_at_pos((52+i),enemyPieces)
                    else:
                        enemiesPresent,_ = get_enemy_at_pos(i,enemyPieces)
                    if enemiesPresent != -1:
                        inDanger = True
                        break
            if inDanger == True:
                newStates.append(DANGER)
                continue

            # STATE NORMAL
            # If no of the other states apply, the state of the current piece is normal
            newStates.append(NORMAL)
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