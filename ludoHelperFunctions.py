import numpy as np
from ludopy.player import enemy_pos_at_pos, get_enemy_at_pos

def isAtHome(piece):
    """
    Checks if a piece is home
    Input:  piece (int) Index of piece to check
    Output: (bool) True if home, False otherwise
    """
    if piece == 0:
        return True
    else:
        return False

def isInApproachToGoal(piece):
    """
    Checks if a piece is in approach to the goal
    Input:  piece (int) Index of piece to check
    Output: (bool) True if in approach to the goal, False otherwise
    """
    if piece >= 53 and piece < 59:
        return True
    else:
        return False

def isInGoal(piece):
    """
    Checks if a piece is in goal
    Input:  piece (int) Index of piece to check
    Output: (bool) True if in the goal, False otherwise
    """
    if piece == 59:
        return True
    else:
        return False

def isOnNormalGlobe(piece):
    """
    Checks if a piece is standing on a normal globe
    Input:  piece (int) Index of piece to check
    Output: (bool) True if standing on a normal globe, False otherwise
    """
    globePos = [1, 9, 22, 35, 48]
    if piece in globePos:
        return True 
    else:
        return False

def isOnEnemyHomeGlobe(piece):
    """
    Checks if piece is standing on an enemy home globe
    Input:  piece (int) Index of piece to check
    Output: (bool) True if standing on an enemy home globe, False otherwise
    """
    enemyHomeGlobePos = [14,27,40]
    if piece in enemyHomeGlobePos:
        return True
    else:
        return False

def isSafeOnEnemyHomeGlobe(piece,enemyPiecesLists):
    """
    Checks if piece is standing on an active enemy players home globe and that it is safe
    Input:  piece (int) Index of piece to check (use playerPieces from game.get_observation)
            enemyPiecesLists (list of lists of int) List of lists of enemy piece positions in the current players frame (use enemyPieces from game.get_observation)
    Output: (bool) True if standing on an active enemy players home globe and the active player has pieces home, False otherwise
    """
    
    # Check if the piece is standing on an enemy home globe
    if isOnEnemyHomeGlobe(piece) == True:
        # Get list of lists of enemies index of the location of the current piece in their respective frames
        enemyIndexes = enemy_pos_at_pos(piece)
        for listIndex,curList in enumerate(enemyIndexes):
            # If there's a 1 in the list, the globe the current piece is on is one of the home globes of the enemy players
            if 1 in curList:
                # Check if that enemy player has any pieces home. If yes, the current pieces isn't safe
                if 0 in enemyPiecesLists[listIndex]:
                    return False
                else:
                    return True
    else:
        return False

def isOnStar(piece):
    """
    Checks if a piece are located on a star
    Input:  pieces (int) Index of the piece(s) to check
    Output: (bool) True is tanding on a star, False otherwise
    """
    if piece == 5 or piece == 12 or piece == 18 or piece == 25 or piece == 31 or piece == 38 or piece == 44 or piece == 51:
        return True
    else:
        return False

def prevStar(starIndex):
    """
    Returns the index of the previous star
    Input:  starIndex (int) Index of the current star
    Output: (int) Index of the previous star
    """
    if starIndex == 5:
        return 51
    elif starIndex == 12:
        return 5
    elif starIndex == 18:
        return 12
    elif starIndex == 25:
        return 18
    elif starIndex == 31:
        return 25
    elif starIndex == 38:
        return 31
    elif starIndex == 44:
        return 38
    else:
        return 44

def enemyInTileRange(tileIndex, enemyPieces, checkEndStar):
    """
    Checks if any of the enemy pieces in pieceLists are in range of tile with index tileIndex
    Input:  tileIndex (int) Index of the tile
            enemyPieces (list of lists of int) List of lists of the enemy pieces to check for (use enemyPieces from game.get_observation)
            checkEndStar (bool) Specifies if a check is performed for the tile being an endstar of a potential enemy piece in range
    Output: (bool) True if any of the pieces are in range, False otherwise 
    """
    for i in range((tileIndex-6),tileIndex):
        # Going backwards, if i is zero or less, get the equivalent index because the table wraps around
        if i < 1:
            i = 52 + i
        # Check if an enemy is at the current tile. If there is, get his player number (0-3) and the number of his piece standing there (0-3)
        enemyNumber, enemyPieceNumber = get_enemy_at_pos(i,enemyPieces)
        if enemyNumber != -1:
            # Grab the index of his piece in range in his frame
            enemyPieceIndex = enemyPieces[enemyNumber][enemyPieceNumber]
            # Find out what the tile is called in that enemies view
            tileEnemyView = enemy_pos_at_pos(tileIndex)
            # If the tile is the end star for the enemy player, and the flag is set, continue searching
            if tileEnemyView[enemyNumber] == 51 and checkEndStar:
                print("In Danger1! At tile ", tileIndex, " Tile in enemy view", tileEnemyView[enemyNumber], "And enemy at ", enemyPieceIndex, " With dist of ", tileEnemyView[enemyNumber] - enemyPieceIndex)
                continue
            # If the enemy index is below 47, the tile is always in range, as the max tile is 52
            if enemyPieceIndex < 47:
                print("In Danger2! At tile ", tileIndex, " Tile in enemy view", tileEnemyView[enemyNumber], "And enemy at ", enemyPieceIndex, " With dist of ", tileEnemyView[enemyNumber] - enemyPieceIndex)
                return True
            # If the enemy index is 47 or above, the only way for the enemy to reach the tile is if it is above the enemy index
            if enemyPieceIndex >= 47 and tileEnemyView[enemyNumber] > enemyPieceIndex:
                print("In Danger3! At tile ", tileIndex, " Tile in enemy view", tileEnemyView[enemyNumber], "And enemy at ", enemyPieceIndex, " With dist of ", tileEnemyView[enemyNumber] - enemyPieceIndex)
                return True
    return False

def isInDanger(piece,otherPieces,enemyPiecesLists):
    """
    Checks if a piece is in danger
    Input:  piece (int) Index of the piece
            otherPieces (list of int) indexes of the other player pieces
            enemyPiecesLists (list of lists of int) List of lists of enemy piece positions in the current players frame (use enemyPieces from game.get_observation)
    Output: (bool) True if in danger, False otherwise
    """
    if piece in otherPieces or isAtHome(piece) or isInGoal(piece) or isInApproachToGoal(piece) or isOnNormalGlobe(piece):
        return False
    if isOnEnemyHomeGlobe(piece):
        if isSafeOnEnemyHomeGlobe(piece, enemyPiecesLists):
            return False
        else:
            return True
    # Check if the current piece is on a star
    if isOnStar(piece):
        # Check if any of the enemy pieces are in range of the previous star
        if enemyInTileRange(prevStar(piece),enemyPiecesLists,True):
            return True
    # Check if current piece is in range of enemy pieces
    if enemyInTileRange(piece,enemyPiecesLists,False):
        return True
    return False

def isSafe(pieces,otherPieces,enemyPiecesLists):

    return not isInDanger(pieces,otherPieces,enemyPiecesLists)

    '''    
        """
        Checks if piece(s) are safe, which they can be in one of three scenarios
        1. If they are standing on the same spot as one of the other pieces from the same player
        2. If the piece is standing on a globe that is not one of the other players home globe 
        3. If the piece is standing on an enemy home globe and that enemy player doesn't have any pieces home
        Input:  pieces (list of int) List of the piece(s) to check (use playerPieces from game.get_observation)
                enemyPieces (list of lists of int) List of lists of enemy piece positions in the current players frame (use enemyPieces from game.get_observation)
        Output: isSafe (list of bool) list of True/False for the piece(s) 
        """
        isSafe = []
        for index,piece in enumerate(pieces):
            otherPieces = np.delete(pieces,index)
            # Check if current piece is at home, in goal or in the approach zone to goal
            if True in isAtHome([piece]) or True in isInGoal([piece]) or True in isInApproachToGoal([piece]):
                isSafe.append(True)
            # Check if current piece is standing together with another of the players pieces
            elif piece in otherPieces:
                isSafe.append(True)
            # Check if current piece is standing on a globe, that is not one of the enemy players home globes
            elif isOnNormalGlobe(piece):
                isSafe.append(True)
            # Check if current piece is standing on an enemy home globe and is in danger
            elif isSafeOnEnemyHomeGlobe(piece,enemyPiecesLists):
                isSafe.append(True)
            else:
                isSafe.append(False)
        return isSafe
    '''

# Returns the distance to the nearest star, if the piece is in range of a star
# Otherwise, -1 is returned
def distToNearestStar(piece):
    if piece < 5 and piece >= 1:
        return 5 - piece
    elif piece < 12 and piece >= 6:
        return 12 - piece
    elif piece < 18 and piece >= 12:
        return 18 - piece
    elif piece < 25 and piece >= 19:
        return 25 - piece
    elif piece < 31 and piece >= 25:
        return 31 - piece
    elif piece < 38 and piece >= 32:
        return 38 - piece
    elif piece < 44 and piece >= 38:
        return 44 - piece
    elif piece < 51 and piece >= 45:
        return 51 - piece
    else:
        return -1