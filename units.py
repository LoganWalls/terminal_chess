import logic

# DEFINE ACTIONS
SWAP = 0
CAPTURE = 1
MOVE = 2
PROMOTE = 3

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

class Unit(object):
    
    def __init__(self, owner, x, y):
        self.owner = owner
        self.owner.add_unit(self)
        self.x = x
        self.y = y
        self.has_moved = False

    def update_position(self, target):
        self.x, self.y = target

    # Returns <bool>: Whether to ignore blocked moves.
    def __handle_block__(self):
        return False

    # Get all possible moves for the unit (ignoring board
    # dimensions and other pieces on the board.
    def __get_all_moves__(self, grid):
        # Get the range of the unit along each a.xis
        move_range = [a * self.speed for a in self.axes]

        moves = []
        # For the distance we can travel on each a.xis...
        for i, distance in enumerate(move_range):
            if distance > 0:
                if i == 0:
                    use_x = 1
                    use_y = 0
                elif i == 1:
                    use_x = 0
                    use_y = 1
                elif i == 2:
                    use_x = 1
                    use_y = 1
                elif i == 3:
                    use_x = -1
                    use_y = 1
                # Add all of the unit's possible moves along that a.xis
                # to the list of moves.
                moves += [[self.x + (j * use_x), self.y + (j * use_y)] for j in range(1, distance + 1)]
                moves += [[self.x - (j * use_x), self.y - (j * use_y)] for j in range(1, distance + 1)]

        return moves

    def move_actions(self, target, grid):
        if grid.get(target[0], target[1]):
            return [CAPTURE, MOVE]
        else:
            return [MOVE]

    # Returns all valid moves for this unit given
    # the 'board's current state and assuming the unit
    # is located at the tile ('self.x', 'self.y') on the board.
    def get_moves(self, grid):
        all_moves = self.__get_all_moves__(grid)
        # Directions where we have encountered
        # another piece blocking our path.
        blocks = []
        # Valid moves.
        moves = []
        for m in all_moves:
            mx, my = m
            move_dir = logic.get_move_direction([self.x, self.y], m)

            # If the move is outside the board...
            if mx < 0 or mx >= grid.width or my < 0 or my >= grid.height:
                # Throw it out.
                continue
            # If the direction is blocked...
            if move_dir in blocks:
                ignore_block = self.__handle_block__()
                # If the block is not ignored, throw out the move.
                if not ignore_block:
                    continue

            # If there's another piece in the square...
            if grid.get(mx, my):
                blocks.append(move_dir)
                # Check if it's a valid move.
                valid_move = self.__handle_interaction__(grid.get(mx, my))
                # If it's valid...
                if valid_move:
                    moves.append(m)
            # Otherwise the space must be empty...
            else:
                # So it's a valid move.
                moves.append(m)

        return moves

    def __handle_interaction__(self, other):
        # If the piece is self.your own piece...
        if other.owner == self.owner:
            return False
        else:
            return True


class King(Unit):
    
    def __init__(self, owner, x, y):
        Unit.__init__(self, owner, x, y)
        self.sprite = u"\u265A"
        self.axes = [1,1,1,1]
        self.speed = 1
        self.owner.king = self

    def __handle_interaction__(self, other):
        # If the piece is self.your own piece...
        if other.owner == self.owner:
            # Check for castling.
            if can_castle(self, other):
                return True
            else:
                return False
        else:
            return True

    def __get_all_moves__(self, grid):
        moves = Unit.__get_all_moves__(self, grid)

        ### Checking for castling:
        # If this unit hasn't moved yet...
        if not self.has_moved:
            # Get the unit objects for the player's rooks.
            if self.owner.direction == 1:
                y = 0
            else:
                y =  grid.height - 1
            queenside_rook = grid.get(0, y)
            kingside_rook = grid.get(grid.width - 1, y)

            if type(queenside_rook) == Rook and not queenside_rook.has_moved:
                if not grid.get(2, y) and not grid.get(3, y):
                    pass

            if type(queenside_rook) == Rook and not queenside_rook.has_moved:
                if not grid.get(5, y) and not grid.get(6, y):
                    pass


        return moves



    def move_actions(self, target, grid):
        other = grid.get(target[0],target[1])
        # Handle castling.
        if other:
            if other.owner == self.owner and type(other) == Rook:
                return [SWAP]
        else:
            return Unit.move_actions(self, target, grid)

class Queen(Unit):
    
    def __init__(self, owner, x, y):
        Unit.__init__(self, owner, x, y)
        self.sprite = u"\u265B"
        self.axes = [1,1,1,1]
        self.speed = 8

class Bishop(Unit):
    
    def __init__(self, owner, x, y):
        Unit.__init__(self, owner, x, y)
        self.sprite = u"\u265D"
        self.axes = [0,0,1,1]
        self.speed = 8

class Knight(Unit):
    
    def __init__(self, owner, x , y):
        Unit.__init__(self, owner, x, y)
        self.sprite = u"\u265E"

    def __get_all_moves__(self, grid):
        return [
                [self.x + 2, self.y + 1], [self.x + 2, self.y - 1],
                [self.x - 2, self.y + 1 ], [self.x - 2, self.y - 1],
                [self.x + 1, self.y + 2], [self.x + 1, self.y - 2],
                [self.x - 1, self.y + 2], [self.x - 1, self.y - 2]
                ]


class Rook(Unit):
    
    def __init__(self, owner, x, y):
        Unit.__init__(self, owner, x, y)
        self.sprite = u"\u265C"
        self.axes = [1,1,0,0]
        self.speed = 8

class Pawn(Unit):
    
    def __init__(self, owner, x, y):
        Unit.__init__(self, owner, x, y)
        self.sprite = u"\u265F"
        self.axes = [0,1,0,0]
        self.speed = owner.direction

    # The pawn requires some different logic to the rest of the pieces
    # so we handle that by 'pre-filtering' the set of moves passed to
    # get_moves() in this function.
    def __get_all_moves__(self, grid):
        moves = []
        owner_dir = self.owner.direction

        # Handle moving forward.
        if not grid.get(self.x, self.y + owner_dir):
            moves.append([self.x, self.y + self.owner.direction])

        # Handle moving two spaces on the first move.
        if not self.has_moved and not grid.get(self.x, self.y + (2 * owner_dir)):
            moves.append([self.x, self.y + (2 * owner_dir)])

        # Handle possible diagonal captures.
        if self.y + owner_dir > 0 and self.y + owner_dir < grid.height:
            if self.x + 1 < grid.width:
                    if grid.get(self.x + 1, self.y + owner_dir):
                        moves.append([self.x + 1, self.y + owner_dir])
            if self.x - 1 > 0:
                if grid.get(self.x - 1, self.y + owner_dir):
                    moves.append([self.x - 1, self.y + owner_dir])

        return moves


    def move_actions(self, target, grid):
        other = grid.get(target[0], target[1])

        actions = Unit.move_actions(self, target, grid)
        if self.owner.direction == 1:
            if target[1] == grid.height - 1:
                actions.append(PROMOTE)
        elif self.owner.direction == -1:
            if target[1] == 0:
                actions.append(PROMOTE)

        return actions
