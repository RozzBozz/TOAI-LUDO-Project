from shutil import move
import ludopy
import numpy as np
import cv2
import AI
from ludoHelperFunctions import *


## AI-loop should look something like
# 0. If the game started (again), set the initial state
# 1. Choose actions and perform
# 2. Let game progress
# 3. Update the state
# 4. Calculate the reward based on this new state
# 5. Update the value of the old state
# 6. Repeat 1-5 until game is finished


game = ludopy.Game()
winnerFound = False

# What the cv2.waitkey function returns when you press one of the four 1, 2, 3, 4 keys
# Might have to be altered to fit your system
ONEKEY = 49
TWOKEY = 50
THREEKEY = 51
FOURKEY = 52
keys = [ONEKEY,TWOKEY,THREEKEY,FOURKEY]

# Stores the index of the previous player
prevPlayer = None

# Stores the round number
round = 0

# Display the table indecies in order to help with moving decision
gameIndexImg = cv2.imread("track.png")
gameIndexImg = cv2.resize(gameIndexImg, (1088,900))
cv2.imshow("Game Indicies", gameIndexImg)
print("-------------------- GAME START --------------------")

while not winnerFound:
    #input_states = StateAndActions()

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
    # If it is the first round, account for the fact, that the dice may be cast up to three times or until a six is rolled, whichever comes first
    if curPlayer == 0 and curPlayer != prevPlayer:
        round = round + 1
        print(f"-------------------- ROUND {round} --------------------")
    prevPlayer = curPlayer

    # Player 4 (index 3) is the real player (chosen so it matches with the video produced)
    # An input is chosen if it is the real players turn
    if curPlayer == 3:
        # Print the current dice roll
        print(f"Dice rolled: {diceRoll}")        
        # Specifies which piece is moved. If no pieces can be moved, it is set to -1
        # If one or more pieces can be moved, this is set to the chosen piece, correpsonding to the index in the movePieces list
        pieceToMoveIndex = None
        # Checks if there are pieces that can be moved
        if len(movePieces) >= 1:
            
            # If all pieces are  home, move the first piece out
            """             
                if not any(playerPieces):
                print("All pieces are home, so moving piece number 1 into the field")
                pieceToMoveIndex = movePieces[0]
            # If only one piece can be moved, move it
            elif len(movePieces) == 1:
                print(f"You can only move piece {movePieces+1} located at board index {playerPieces[movePieces[0]]}, so moving that")
                pieceToMoveIndex = movePieces[0]
            else: """
            #print("-----Enemy pieces:-----\n", enemyPieces)
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
            pieceToMoveIndex = movePieces[np.random.randint(0, len(movePieces))]
        else:
            pieceToMoveIndex = -1

    _, _, _, _, _, winnerFound = game.answer_observation(pieceToMoveIndex)

    if winnerFound:
        winningPlayer = curPlayer

print("-------------------- GAME FINISHED --------------------")
print(f"Player {winningPlayer+1} won!")
if winningPlayer == 3:
    print("Congratulations! You won!")
else:
    print("You lost, better luck next time!")
print("Saving history to numpy file")
game.save_hist(f"game_history.npy")
print("Saving game video")
game.save_hist_video(f"game_video.avi")