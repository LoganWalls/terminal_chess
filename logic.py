# DEFINE DIRECTIONS
HORIZ = 0
VERT = 1
DIAG_R = 2
DIAG_L = 3

# DEFINE CASTLE SIDES
QUEENSIDE = 0
KINGSIDE = 1

# DEFINE
# Grid Dimensions
GRID_HEIGHT = 8
GRID_WIDTH = 8

# Player IDs
PLAYER1 = 0
PLAYER2 = 1

# Actions
CASTLE = 0
PROMOTE = 1


'''
    Helper functions for game logic.
'''
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

def hypothetical_move(cur_state, origin, target):
    ox, oy = origin
    tx, ty = target
    unit = cur_state.grid.get(ox, oy)
    new_grid = copy(cur_state.grid)
    new_grid.set(unit, tx, ty)
    new_grid.set(None, ux, uy)
    
    p1 = cur_state.player1
    p2 = cur_state.player2

    return State(grid, 0)

def crosses_check(cur_state, origin, target):
    pass

# Assumes both pieces hace the same owner.
def castle_check(unit, target, other):
    tx, ty = target

    # The other piece must be a rook.
    if type(other).__name__ == 'Rook':
        # If neither piece has moved then it is safe to assume
        # they are both on the player's first rank.
        if unit.has_moved == other.has_moved == False:
            if tx == 0:
                # Check for check
                pass
            elif tx == GRID_WIDTH - 1:
                # Check for check
                pass
            else:
                return None