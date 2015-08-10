from logic import *

class Unit(object):
    
    def __init__(self, owner, direction):
        self.owner = owner
        self.has_moved = False
        self.direction = direction

    '''
    Function:
        Get all possible moves for the unit (ignoring board
        dimensions and other pieces on the board.
    Parameters:
        origin <[int, int]>: An [x, y] coordinate pair of the unit's
                                current grid location.
        state <State>: The current game-state object.
    Returns:
        <[ [int, int], ...]>: A list of target coordinate pairs for all of 
                                the moves this unit might possibly make.
                                (Before considering path obstructions, etc.)
    '''
    def __get_all_moves__(self, origin, state):
        x, y = origin
        grid = state.grid
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
                moves += [[x + (j * use_x), y + (j * use_y)] for j in range(1, distance + 1)]
                moves += [[x - (j * use_x), y - (j * use_y)] for j in range(1, distance + 1)]

        return moves

    '''
    Function:
        Returns all valid moves for this unit given
        the 'board's current state and assuming the unit
        is located at the tile ('x', 'y') on the board.
    Parameters:
        origin <[int, int]>: An [x, y] coordinate pair of the unit's 
                             current grid position.
        state <State>: The current game-state object.
    Returns:
        <[[int, int], [int, int], dict]]>: 

                    A list of 'move' triplets [origin, target, flags]:
                        origin: [x, y] coordinate pair for the unit's
                                starting grid position.
                        target: [x, y] coordinate pair for the unit's
                                destination grid position.
                        flag:   A dictonary with any special information
                                about the move (castling, pawn promotion, etc.)
                                (flag is None if there is no special behavior)
    '''
    def get_moves(self, origin, state):
        grid = state.grid
        all_moves = self.__get_all_moves__(origin, state)
        ox, oy = origin
        # Directions where we have encountered
        # another piece blocking our path.
        blocks = []
        # Valid moves.
        moves = []
        for target in all_moves:
            tx, ty = target
            move_dir = get_move_direction(origin, target)

            # If the move is outside the board...
            if tx < 0 or tx >= grid.width or ty < 0 or ty >= grid.height:
                # Throw out the move.
                continue
            # If the direction is blocked...
            if move_dir in blocks:
                # Throw out the move.
                continue

            # If there's another piece in the square...
            other = grid.get(tx, ty)
            if other is not None:
                # Note that this direction is blocked.
                # (But don't throw out the move: we want to
                #  be able to capture the first unit that 
                #  us if applicable blocks).
                blocks.append(move_dir)


            # See how to handle the move.
            handling = self.__handle_interaction__(origin, target, other)
            # If it's valid...
            if handling is not None:
                moves.append(handling)

        return moves

    def __handle_interaction__(self, origin, target, other):
        flag = None

        # If the piece is your own piece...
        if other and other.owner == self.owner:
            return None
        else:
            return [origin, target, flag]


class King(Unit):
    
    def __init__(self, owner, direction):
        Unit.__init__(self, owner, direction)
        self.sprite = u"\u265A"
        self.axes = [1,1,1,1]
        self.speed = 1

    def __handle_interaction__(self, origin, target, other):
        if other:
            # If the piece is your own piece...
            if other.owner == self.owner:
                # Check for castling.
                castle_side = castle_check(self, target, other)
                if castle_side:
                    flag = {'action':CASTLE, 'side':castle_side}
                    return [origin, target, flag]
                else:
                    return None
        else:
            return [origin, target, None]

    def __get_all_moves__(self, origin, state):
        x, y = origin
        grid = state.grid
        moves = Unit.__get_all_moves__(self, origin, state)

        return moves
        ### Checking for castling:
        # If this unit hasn't moved yet and we're not in check...
        if not self.has_moved and not state.in_check(self.owner):
            # Get the unit objects for the player's rooks.
            if self.direction == 1:
                y = 0
            else:
                y =  grid.height - 1
            queenside_rook = grid.get(0, y)
            kingside_rook = grid.get(grid.width - 1, y)

            if type(queenside_rook).__name__ == 'Rook' and not queenside_rook.has_moved:
                # If there are no units blocking the way.
                if not grid.get(3, y) and not grid.get(2, y):
                    
                    moves.append([2, y])

            if type(kingside_rook).__name__  == 'Rook' and not kingside_rook.has_moved:
                # If there are no units blocking the way.
                if not grid.get(5, y) and not grid.get(6, y):
                    moves.append([6, y])

        return moves

class Queen(Unit):
    
    def __init__(self, owner, direction):
        Unit.__init__(self, owner, direction)
        self.sprite = u"\u265B"
        self.axes = [1,1,1,1]
        self.speed = 8

class Bishop(Unit):
    
    def __init__(self, owner, direction):
        Unit.__init__(self, owner, direction)
        self.sprite = u"\u265D"
        self.axes = [0,0,1,1]
        self.speed = 8

class Knight(Unit):
    
    def __init__(self, owner, direction):
        Unit.__init__(self, owner, direction)
        self.sprite = u"\u265E"

    def __get_all_moves__(self, origin, state):
        x, y = origin
        return [
                [x + 2, y + 1], [x + 2, y - 1],
                [x - 2, y + 1 ], [x - 2, y - 1],
                [x + 1, y + 2], [x + 1, y - 2],
                [x - 1, y + 2], [x - 1, y - 2]
                ]

class Rook(Unit):
    
    def __init__(self, owner, direction):
        Unit.__init__(self, owner, direction)
        self.sprite = u"\u265C"
        self.axes = [1,1,0,0]
        self.speed = 8

class Pawn(Unit):
    
    def __init__(self, owner, direction):
        Unit.__init__(self, owner, direction)
        self.sprite = u"\u265F"
        self.axes = [0,1,0,0]
        self.speed = direction

    # The pawn requires some different logic to the rest of the pieces
    # so we handle that by 'pre-filtering' the set of moves passed to
    # get_moves() in this function.
    def __get_all_moves__(self, origin, state):
        x, y = origin
        grid = state.grid
        moves = []

        # Handle moving forward.
        if y + self.direction > 0 and y + self.direction < GRID_HEIGHT:
            if not grid.get(x, y + self.direction):
                moves.append([x, y + self.direction])

        # Handle moving two spaces on the first move.
        if y + (2 * self.direction) > 0 and y + (2 * self.direction) < GRID_HEIGHT:
            if not self.has_moved and not grid.get(x, y + (2 * self.direction)):
                moves.append([x, y + (2 * self.direction)])

        # Handle possible diagonal captures.
        if y + self.direction > 0 and y + self.direction < grid.height:
            if x + 1 < grid.width:
                    if grid.get(x + 1, y + self.direction):
                        moves.append([x + 1, y + self.direction])
            if x - 1 > 0:
                if grid.get(x - 1, y + self.direction):
                    moves.append([x - 1, y + self.direction])

        return moves


    def __handle_interaction__(self, origin, target, other):
        tx, ty = target

        # If the piece is your own piece...
        if other and other.owner == self.owner:
            return None
        else:
            flag = None
            # Check for promotion.
            if self.direction == 1:
                if ty == GRID_HEIGHT - 1:
                    flag = {'action':PROMOTE}
            elif self.direction == -1:
                if ty == 0:
                    flag = {'action':PROMOTE}

            return [origin, target, flag]
