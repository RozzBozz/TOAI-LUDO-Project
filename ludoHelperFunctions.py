import numpy as np
from ludopy.player import enemy_pos_at_pos, get_enemy_at_pos

# For states

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

def isSafeOnEnemyHomeGlobe(piece,enemyPieces):
    """
    Checks if piece is standing on an active enemy players home globe and that it is safe
    Input:  piece (int) Index of piece to check (use playerPieces from game.get_observation)
            enemyPieces (list of lists of int) List of lists of enemy piece positions in the current players frame (use enemyPieces from game.get_observation)
    Output: (bool) True if standing on an active enemy players home globe and the active player has pieces home, False otherwise
    """
    
    # Check if the piece is standing on an enemy home globe
    if isOnEnemyHomeGlobe(piece) == True:
        # Get list of lists of enemies index of the location of the current piece in their respective frames
        enemyIndexes = enemy_pos_at_pos(piece)
        for listIndex,curList in enumerate(enemyIndexes):
            # If there's a 1 in the list, the globe that the current piece is on is one of the home globes of the enemy players
            if 1 in curList:
                # Check if that enemy player has any pieces home. If yes, the current pieces isn't safe
                if 0 in enemyPieces[listIndex]:
                    return False
                else:
                    return True
    else:
        return False

def isOnStar(piece):
    """
    Checks if a piece are located on a star
    Input:  pieces (int) Index of the piece(s) to check
    Output: (bool) True is standing on a star, False otherwise
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
                continue
            # If the enemy index is below 47, the tile is always in range, as the max tile is 52
            if enemyPieceIndex < 47:
                return True
            # If the enemy index is 47 or above, the only way for the enemy to reach the tile is if it is above the enemy index
            if enemyPieceIndex >= 47 and tileEnemyView[enemyNumber] > enemyPieceIndex:
                return True
    return False

def isInDanger(piece,otherPieces,enemyPieces):
    """
    Checks if a piece is in danger
    Input:  piece (int) Index of the piece
            otherPieces (list of int) indexes of the other player pieces
            enemyPieces (list of lists of int) List of lists of enemy piece positions in the current players frame (use enemyPieces from game.get_observation)
    Output: (bool) True if in danger, False otherwise
    """
    if piece in otherPieces or isAtHome(piece) or isInGoal(piece) or isInApproachToGoal(piece) or isOnNormalGlobe(piece):
        return False
    if isOnEnemyHomeGlobe(piece):
        if isSafeOnEnemyHomeGlobe(piece, enemyPieces):
            return False
        else:
            return True
    # Check if the current piece is on a star
    if isOnStar(piece):
        # Check if any of the enemy pieces are in range of the previous star
        if enemyInTileRange(prevStar(piece),enemyPieces,True):
            return True
    # Check if current piece is in range of enemy pieces
    if enemyInTileRange(piece,enemyPieces,False):
        return True
    return False

def isSafe(pieces,otherPieces,enemyPieces):
    """
    Inverse of isInDanger, see that fro documentation
    """
    return not isInDanger(pieces,otherPieces,enemyPieces)

# For Actions

def nextStar(tile):
    '''
    Returns the index of the next star, -1 if there isn't any or if the tile is at home
    Input: piece (int) Index of the piece to check
    Output: (int) Index of the next star, -1 if there isn't any, or if the tile is at home
    '''
    if not isAtHome(tile) and tile < 5:
        return 5
    elif tile < 12:
        return 12
    elif tile < 18:
        return 18
    elif tile < 25:
        return 25
    elif tile < 31:
        return 31
    elif tile < 38:
        return 38
    elif tile < 44:
        return 44
    elif tile < 51:
        return 51
    else:
        return -1

def canMoveOut(piece,diceRoll):
    """
    Checks if the piece can move out from home
    Input:  piece (int) Index of the piece to check
            diceRoll (int) What the dice rolled
    Output: (bool) True if the piece can move out from home, False otherwise
    """
    if diceRoll == 6 and piece == 0:
        return True
    else:
        return False

def numberOfEnemiesAtTile(tile,enemyPieces):
    """
    Get the number of enemies at the tile
    Input:  piece (int) Index of the piece to check
            enemyPieces (list of lists of int) List of lists of the enemy pieces to check for (use enemyPieces from game.get_observation)
    Output (int) Number of enemies at the tile
    """
    _, enemyPieceNumber = get_enemy_at_pos(tile,enemyPieces)
    return len(enemyPieceNumber)

def canAttack(piece, enemyPieces, diceRoll):
    """
    Check if the piece can move to an enemy piece that is not safe
    Input:  piece (int) Index of the piece to check
            enemyPieces (list of lists of int) List of lists of the enemy pieces to check for (use enemyPieces from game.get_observation)
            diceRoll (int) What the dice rolled
    Output (bool) True if the piece can attack an enemy piece, False otherwise
    """

    nextTile = piece + diceRoll
    # Piece cannot attack if at home, at goal or approaching goal, or if the next tile is a globe
    if not isAtHome(piece) and not isInApproachToGoal(piece) and not isInGoal(piece) and not isOnNormalGlobe(nextTile) and not isOnEnemyHomeGlobe(nextTile):
        # If the next tile is not a star, and there is one enemy on it, the piece can attack
        if not isOnStar(nextTile) and numberOfEnemiesAtTile(nextTile,enemyPieces) == 1:
            return True
        # If the next tile is a star, and either of the  tiles have one enemy on it, it can attack
        elif isOnStar(nextTile) and (numberOfEnemiesAtTile(nextTile,enemyPieces) == 1 or numberOfEnemiesAtTile(nextStar(nextTile),enemyPieces) == 1):
            return True   
    return False

def canMove(piece):
    """
    Check if the piece is not at home or in goal
    Input:  piece (int) Index of the piece to check
    Output (bool) True if the piece can attack an enemy piece, False otherwise
    """
    if isAtHome(piece) or isInGoal(piece):
        return False
    else:
        return True

def canMoveStar(piece,enemyPieces,diceRoll):
    """
    Checks if the piece can go safely, i.e without being knocked home, to the nearest star with the current dice roll.
    Input:  piece (int) Index of the piece to check
            enemyPieces (list of lists of int) List of lists of the enemy pieces to check for (use enemyPieces from game.get_observation)
            diceRoll (int) What the dice rolled
    Output (bool) True if the piece can move to the nearest star safely, False otherwise
    """

    # Cannot move to the next star 

    nextTile = piece + diceRoll
    # Piece cannot move to a star if the next tile is ot a star, or it is home, in approach to goal or in goal
    if nextTile == nextStar(piece) and not isAtHome(piece) and not isInApproachToGoal(piece) and not isInGoal(piece):
        # Check that both star tiles are safe to land on
        if numberOfEnemiesAtTile(nextTile,enemyPieces) < 2 and numberOfEnemiesAtTile(nextStar(nextTile),enemyPieces) < 2:
            return True
    return False

def canMoveHome(piece,diceRoll):
    """
    Checks if the piece can go to the goal
    Input:  piece (int) Index of the piece to check
            diceRoll (int) What the dice rolled
    Output (bool) True if the piece can move to the goal, False otherwise
    """
    tile = piece + diceRoll
    # If the new tile matches the goal tile or the last star, it can move to goal
    if tile == 59 or tile == 51:
        return True
    else:
        return False

def canMoveSafe(piece,otherPieces,diceRoll,enemyPieces):
    """
    Checks if the piece can move to the next tile such that it is safe, which can be achieved in four ways:
    1. Go to neutral globe with no enemies
    2. Go to another friendly piece
    3. Go to the goal zone
    4. Go an enemy globe who doesn't have anymore pieces home
    5. Go to a star, which leads to another friendly piece
    Input:  piece (int) Index of the piece to check
            otherPieces (list of int) Indecies of the other player pieces
            enemyPieces (list of lists of int) List of lists of the enemy pieces to check for (use enemyPieces from game.get_observation)
            diceRoll (int) What the dice rolled
    Output (bool) True if the piece can move to safely to the next tile, False otherwise
    """

    # What about the end star? Also, i dont account for jumps if the tile is a star

    # Cannot move to a safe location if the piece is at home. This action is instead called move out
    if isAtHome(piece):
        return False

    nextTile = piece + diceRoll
    if isOnNormalGlobe(nextTile) and numberOfEnemiesAtTile(nextTile,enemyPieces) == 0:
        return True
    elif nextTile in otherPieces:
        return True
    elif isInApproachToGoal(nextTile):
        return True
    elif isSafeOnEnemyHomeGlobe(nextTile):
        return True
    elif nextStar(piece) == nextTile and nextStar(nextTile) in otherPieces:
        return True
    return False
    