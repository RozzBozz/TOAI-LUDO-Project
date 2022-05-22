from shutil import move
import ludopy
import numpy as np
import cv2
from AI import *
from ludoHelperFunctions import *

# Idea: Possible multiplayer support, but out of scope of the project

# ---------- CONTROLS ----------
# Which player number is the AI (If number 4 is chosen, it matches with the game video produced, if that is enabled)
playerNumber = 1
# How many games should be played for each test?
numberOfGames = 101
# How many opponents?
numberOfOpponents = 3
# Should the Q-table of the AI be reset after a test?
resetQTableAfterTest = True
# Are the enemies random players or semi smart players?
randomEnemies = True # (NOT IMPLEMENTED)
# Should the AI start from scratch, or just exploit the current knowledge (Q-table)?
shouldLearn = False
# If the AI is training, should it start from scratch?
shouldStartOver = False

# Values to be tested
epsilons = [0.1, 0.5] # , 0.9
alphas = [0.25] # , 0.5, 0.75
gammas = [0.5] # , 0.7, 0.9

for epsilon in epsilons:
    for alpha in alphas:
        for gamma in gammas:

            # Initialization of AI
            QTableFileName = "QTables/epsilon{}alpha{}gamma{}.npy".format(epsilon,alpha,gamma)
            dataFileName = "dataFiles/epsilon{}alpha{}gamma{}.txt".format(epsilon,alpha,gamma)
            winRatesFileName = "winRates/epsilon{}alpha{}gamma{}.txt".format(epsilon,alpha,gamma)
            if shouldStartOver:
                print("---------- Currently LEARNING with values epsilon", epsilon, "alpha", alpha, "gamma", gamma, "----------")
                ludoAI = AI(epsilon=epsilon, alpha=alpha, gamma=gamma, newQTable = True, newDataFile = True)
            else:
                if not shouldLearn:
                    epsilon = 0
                print("---------- Currently TESTING with values epsilon", epsilon, "alpha", alpha, "gamma", gamma, "----------")
                # Create the string for the Q-table and data-file the AI should use
                ludoAI = AI(QTableFileName = QTableFileName, dataFileName = dataFileName, winRatesFileName=winRatesFileName, epsilon=epsilon, alpha=alpha, gamma=gamma, loadOldWinrates= True)

            for gameNumber in range(1,numberOfGames+1):

                # Print every 100th game
                if gameNumber % 100 == 0:
                    print("---------- Currently playing game number", gameNumber, "of", numberOfGames, "----------")

                # Initialize game
                if numberOfOpponents == 3:
                    game = ludopy.Game()
                else:
                    ghostPlayers = [1,2,3,4]
                    ghostPlayers = np.delete(ghostPlayers,playerNumber)
                    for i in range(0,numberOfOpponents-1):
                        ghostPlayers = np.delete(ghostPlayers,i)
                    game = ludopy.Game(ghostPlayers)
                winnerFound = False
                # Stores the index of the previous player
                prevPlayer = None
                # Stores the round number of the current game
                round = 0
                # Reset the state of the AI
                ludoAI.reset()
                # Specifies, that a state update, reward calculation and Q-table update shouldn't be done in the first round
                doSRupdate = False

                #print("-------------------- START OF GAME", gameNumber, "OF", numberOfGames,"--------------------")

                while not winnerFound:

                    # Observe the game state. A get_obersvation call must be answered be a answer_observation call before it can be called again
                    # diceRoll (int): Dice roll for the current player
                    # movePieces (list of up to four ints): Index of the pieces that can be moved. E.g piece 0, 1, 2 or 3 (They are zero-indexed)
                    # playerPieces (list of four ints): Indecies of the current players pieces on the board. Corresponds to the numeration of the game board
                    # enemyPieces: (list of four ints): Indecies of the enemy pieces on the board. The indecies are given in teh players respective frames, NOT the current player
                    # playerWinner (bool): True, if the current player is the winner
                    # winnerFound (bool): True, if a winner has been found
                    # curPlayer (int): Index of the current player
                    (diceRoll, movePieces, playerPieces, enemyPieces, playerWinner, winnerFound), curPlayer = game.get_observation()
                    allPieces = enemyPieces
                    allPieces = np.append(enemyPieces, [playerPieces], axis=0)

                    # The first player (index 0) starts a round
                    # If it is the first round, account for the fact, that a player may cast the dice multiple times in a row during start, or if he/she hits a six
                    if curPlayer == 0 and curPlayer != prevPlayer:
                        round = round + 1
                    prevPlayer = curPlayer

                    # Input is allowed if it is the human/AI players turn
                    if curPlayer == playerNumber-1:
                        # Specifies which piece is moved. If no pieces can be moved, it is set to -1
                        # If one or more pieces can be moved, this is set to the chosen piece, correpsonding to the index in the movePieces list
                        pieceToMoveIndex = None
                        if doSRupdate:
                            # Start by updating the state of the AI
                            ludoAI.updateState(pieces=playerPieces,enemyPieces=enemyPieces)
                            if shouldLearn:
                                # Estimate the reward for being in this state
                                ludoAI.calculateReward(round=round,pieces=playerPieces)
                                # Update the Q-value of the previous state
                                ludoAI.updateQValue()
                        doSRupdate = True
                        # Select an action
                        ludoAI.selectAction(diceRoll=diceRoll, pieces=playerPieces, enemyPieces=enemyPieces)
                        pieceToMoveIndex = ludoAI.getPieceIndexMove()            
                    else:
                        if len(movePieces):
                            if randomEnemies:
                                pieceToMoveIndex = movePieces[np.random.randint(0, len(movePieces))]
                            else:
                                pass
                        else:
                            pieceToMoveIndex = -1

                    _, _, _, _, _, winnerFound = game.answer_observation(pieceToMoveIndex)

                    if winnerFound:
                        winningPlayer = curPlayer

                #print("-------------------- GAME", gameNumber, "OF", numberOfGames, "FINISHED --------------------")

                ludoAI.addGamePlayed()
                if winningPlayer == playerNumber-1:
                    ludoAI.addWin()
                ludoAI.updateWinRates()
                #print("Number of games played:", ludoAI.getNumberOfGamesPlayed())
                #print("Number of games won:", ludoAI.getNumberOfGamesWon())
                #print("Current AI win rate: ", ludoAI.getCurWinRate() * 100, "%")

            ludoAI.saveQTable(QTableFileName)
            ludoAI.saveDataFile(dataFileName)
            ludoAI.saveWinRates(winRatesFileName)