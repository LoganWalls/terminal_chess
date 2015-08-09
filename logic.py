'''
    Helper functions for game logic.
'''

# DEFINE DIRECTIONS
HORIZ = 0
VERT = 1
DIAG_R = 2
DIAG_L = 3

# Determine the direction of a move relative to the unit.
def get_move_direction(origin, destination):
    ox, oy = origin
    dx, dy = destination
    diff_x = dx - ox
    diff_y = dy - oy

    # Diagonal case.
    if abs(diff_x) == abs(diff_y):
        if diff_x < 0:
            if diff_y > 0:
                return DIAG_L
            elif diff_y < 0:
                return -DIAG_L

        elif diff_x > 0:
            if diff_y > 0:
                return DIAG_R
            elif diff_y < 0:
                return -DIAG_R

    # Horizontal case.
    elif abs(diff_x) > abs(diff_y):
        if diff_x > 0:
            return HORIZ
        else:
            return -HORIZ

    # Vertical case.
    elif abs(diff_y) > abs(diff_x):
        if diff_y > 0:
            return VERT
        else:
            return -VERT

def valid_units(self):
    return [
        'king',
        'queen',
        'bishop',
        'knight',
        'rook',
        'pawn'
    ]

# Assumes both pieces hace the same owner.
def can_castle(unit, other):

    # The other piece must be a rook.
    if type(other) == Rook:
        # If neither piece has moved then it is safe to assume
        # they are both on the player's first rank.
        if this.has_moved == other.has_moved == False:
            pass