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
numberOfGames = 1000
# How many opponents?
numberOfOpponents = 3
# Are the enemies random players or semi smart players?
randomEnemies = True # (NOT IMPLEMENTED)
# Should the AI start from scratch, or just exploit the current knowledge (Q-table)?
shouldLearn = False

# Values to be tested
epsilon = 1
epsilonDecays = [0.02] # [%]
alphas = [0.5] # 
gammas = [0.4] # 

for epsilonDecay in epsilonDecays:
    for alpha in alphas:
        for gamma in gammas:
            for i in range(0,1):
                # Initialization of AI
                if shouldLearn:
                    QTableFileName = "QTables/epsilonDecay{}alpha{}gamma{}.npy".format(epsilonDecay,alpha,gamma)
                else:
                    QTableFileName = "QTable1Player.npy"
                dataFileName = "dataFiles/epsilonDecay{}alpha{}gamma{}.txt".format(epsilonDecay,alpha,gamma)
                winRatesFileName = "winRates/epsilonDecay{}alpha{}gamma{}.txt".format(epsilonDecay,alpha,gamma)
                deltaQsFileName = "deltaQs/epsilonDecay{}alpha{}gamma{}.txt".format(epsilonDecay,alpha,gamma)
                ludoAI = AI(QTableFileName, alpha, gamma, epsilon, epsilonDecay)

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
                    if shouldLearn:
                        ludoAI.reset()
                    # Specifies, that a state update, reward calculation and Q-table update shouldn't be done in the first round
                    doSRupdate = False

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
                            pieceToMoveIndex = ludoAI.onePass(diceRoll,playerPieces,enemyPieces,shouldLearn)
                            
                            #img = ludopy.visualizer.make_img_of_board(allPieces, diceRoll, 3, round)
                            #img = cv2.resize(img, (1088,900))
                            #cv2.imshow("Current state of the board", img)
                            #key = cv2.waitKey(0)
                            #cv2.destroyWindow("Current state of the board")
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
                    ludoAI.addCurWinRate()
                    ludoAI.addCurDeltaQSum()
                    # Decay the epsilon-value after each game 
                    if shouldLearn:
                        ludoAI.decayEpsilon(epsilonDecay)
                    #print("Number of games played:", ludoAI.getNumberOfGamesPlayed())
                    #print("Number of games won:", ludoAI.getNumberOfGamesWon())
                    #print("Current AI win rate: ", ludoAI.getCurWinRate() * 100, "%")

                ludoAI.saveQTable(QTableFileName)
                ludoAI.saveDataFile(dataFileName)
                ludoAI.saveWinRates(winRatesFileName)
                if shouldLearn:
                    ludoAI.saveDeltaQs(deltaQsFileName)