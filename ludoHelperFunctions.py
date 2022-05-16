
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