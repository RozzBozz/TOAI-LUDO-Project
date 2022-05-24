from shutil import move
import ludopy
import numpy as np
import cv2
from AI import *
from ludoHelperFunctions import *

# Idea: Possible multiplayer support, but out of scope of the project

# ---------- CONTROLS ----------
# Which player number is the AI/human? (If number 4 is chosen, it matches with the game video produced, if that is enabled)
playerNumber = 1
# How many games should be played?
numberOfGames = 1000
# How many opponents?
numberOfOpponents = 3
# Is the AI playing?
isAI = False
# Should the AI train, or just exploit the current knowledge (Q-table)?
shouldLearn = False
# Values for the hyper parameters of the AI (epsilon, alpha, gamma)
parameters = [0.1, 0.5, 0.9]
# If the human is playing, should moves be performed if they are the only choice?
autoMove = False
# Should the game history be saved? (Not recommended if numberOfGames > 1)
saveGameHistory = False
# Are the enemies random players or semi smart players?
randomEnemies = True # (NOT IMPLEMENTED)

# Initialization of AI/

ludoAI = AI("", parameters[0], parameters[1], parameters[2])
if isAI == True:
    QTableFileName = "QTables/epsilon{}alpha{}gamma{}.npy".format(parameters[0],parameters[1],parameters[2])
    dataFileName = "dataFiles/epsilon{}alpha{}gamma{}.txt".format(parameters[0],parameters[1],parameters[2])
    winRatesFileName = "winRates/epsilon{}alpha{}gamma{}.txt".format(parameters[0],parameters[1],parameters[2])
    if shouldLearn:
        ludoAI = AI(QTableFileName, parameters[0], parameters[1], parameters[2])
        print("---------- Currently LEARNING with values epsilon", parameters[0], "alpha", parameters[1], "gamma", parameters[2], "----------")
    else:
        ludoAI = AI(QTableFileName, 0, parameters[1], parameters[2])
        print("---------- Currently TESTING AIs trained with values epsilon", parameters[0], "alpha", parameters[1], "gamma", parameters[2], "----------")
else:
    # To keep track of how many wins the current player has
    winCounter = 0
    # Display the table indecies in order to help with moving decision
    gameIndexImg = cv2.imread("track.png")
    gameIndexImg = cv2.resize(gameIndexImg, (1088,900))
    cv2.imshow("Game Indicies", gameIndexImg)
    # Define key-presses for the human
    # What the cv2.waitkey function returns when you press one of the four 1, 2, 3, 4 keys
    # Might have to be altered to fit your system
    ONEKEY = 49
    TWOKEY = 50
    THREEKEY = 51
    FOURKEY = 52
    keys = [ONEKEY,TWOKEY,THREEKEY,FOURKEY]

for gameNumber in range(1,numberOfGames+1):

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
    # If the round is zero, and the player is an AI, reset the state of the AI
    
    if isAI == True:
        ludoAI.reset()

    # Print every 100th game
    if isAI and gameNumber % 100 == 0:
        print("---------- Currently playing game number", gameNumber, "of", numberOfGames, "----------")
    elif not isAI:
        print("-------------------- START OF GAME", gameNumber, "OF", numberOfGames,"--------------------")

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
            # Only print round number if the player is human
            if isAI == False:
                print(f"-------------------- ROUND {round} --------------------")
        prevPlayer = curPlayer

        # Input is allowed if it is the human/AI players turn
        if curPlayer == playerNumber-1:
            # Specifies which piece is moved. If no pieces can be moved, it is set to -1
            # If one or more pieces can be moved, this is set to the chosen piece, correpsonding to the index in the movePieces list
            pieceToMoveIndex = None
            # Print the rolled die, if the player is human
            if isAI == False:
                print(f"Dice rolled: {diceRoll}")
            
            if isAI == True:
                    pieceToMoveIndex = ludoAI.onePass(diceRoll,playerPieces,enemyPieces,shouldLearn=shouldLearn) 
            # Human player
            else:
                # Checks if there are pieces that can be moved
                if len(movePieces) >= 1:
                    # If all pieces are at either home or end, move one out
                    if autoMove == True:
                        canMove = False
                        for piece in playerPieces:
                            if not isAtHome(piece) and not isInGoal(piece):
                                canMove = True
                                break
                        if canMove == False:
                            print("All playable pieces are home, so moving piece number 1 into the field")
                            pieceToMoveIndex = movePieces[0]
                        # If only one piece can be moved, move it
                        elif len(movePieces) == 1:
                            print(f"You can only move piece {movePieces+1} located at board index {playerPieces[movePieces[0]]}, so moving that")
                            pieceToMoveIndex = movePieces[0]
                    # No move found in autoMove
                    if pieceToMoveIndex == None:
                    # Used for debugging states and actions
                        print("-----Enemy pieces:-----\n", enemyPieces)
                        print(ludoAI.getState(playerPieces,enemyPieces))
                    #for index,piece in enumerate(playerPieces):
                    #    otherPieces = np.delete(playerPieces,index)
                    #    print("Piece", index+1, "Danger: ", isInDanger(piece,otherPieces,enemyPieces))
                    #actions = AI.getAvaliableActions(playerPieces,diceRoll,enemyPieces)
                    #print(actions)
                        print("Choose one of the following pieces to move, by pressing the corresponding number on your keyboard")
                        for pieceNumber in movePieces:
                            print(f"Piece {pieceNumber+1} located at index {playerPieces[pieceNumber]}")
                        img = ludopy.visualizer.make_img_of_board(allPieces, diceRoll, 3, round)
                        img = cv2.resize(img, (1088,900))
                        cv2.imshow("Current state of the board", img)
                        # Create list of key values that correspond to the key value needed to move the piece at the same index in the movePieces list
                        moveKeys = []
                        for i in range(len(movePieces)):
                            moveKeys.append((movePieces[i] + ONEKEY))
                        # Wait until any key is pressed
                        while pieceToMoveIndex == None:
                            key = cv2.waitKey(0)
                            # Check if a valid key is chosen
                            if key in moveKeys:
                                print(f"Moving piece number {key-ONEKEY+1}")
                                cv2.destroyWindow("Current state of the board")
                                for moveIndex,moveKey in enumerate(moveKeys):
                                    if key == moveKey:
                                        pieceToMoveIndex = movePieces[moveIndex]
                                        break
                            else:
                                print(f"Read key value {key}, expected on of the following possibilites: {moveKeys}. Try again")
                else:
                    pieceToMoveIndex = -1   
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
    
    if isAI == False:
        print("-------------------- GAME", gameNumber, "OF", numberOfGames, "FINISHED --------------------")
        # Print celebratory text
        print(f"Player {winningPlayer+1} won!")
        if winningPlayer == playerNumber-1:
            winCounter = winCounter + 1
            print("Congratulations! You won!")
        else:
            print("You lost, better luck next time!")
        print("You have currently won", winCounter, "out of", numberOfGames, "games!")
    else:
        ludoAI.addGamePlayed()
        if winningPlayer == playerNumber-1:
            ludoAI.addWin()
    
    if saveGameHistory == True:
        print("Saving history to numpy file")
        game.save_hist(f"game_history.npy")
        print("Saving game video")
        game.save_hist_video(f"game_video.avi")

if isAI == True:
    ludoAI.saveQTable(QTableFileName)
    ludoAI.saveDataFile(dataFileName)
    ludoAI.saveWinRates(winRatesFileName)
    