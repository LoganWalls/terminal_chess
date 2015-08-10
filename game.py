import string
from logic import *
from units import *
from rendering import Renderer
from copy import copy

class State(object):

    def __init__(self, grid, turn, p1_caps=[], p2_caps=[]):
        # Game information.
        self.grid = grid
        self.p1_check = self.__in_check__(PLAYER1)
        self.p2_check = self.__in_check__(PLAYER2)
        
        # Units each player has captured.
        self.p1_caps = p1_caps
        self.p2_caps = p2_caps

        # The number of turns which have passed.
        self.turn = turn

    # Returns whether or not the given player is in check
    # in this state.
    def __in_check__(self, player):
        return False
        #  ------ get KING ------

        if player == PLAYER1:
            opponent = PLAYER2
        else:
            opponent = PLAYER1

        opponent_moves = self.get_player_moves(opponent)
        
        for m in opponent_moves:
            x, y = m[0]
            # If taking the King is a valid move for
            # the opponent...
            if self.grid.get(x, y) == king:
                return True

        return False

    def in_check(self, player):
        if player == PLAYER1:
            return self.p1_check
        else:
            return self.p2_check

    # Gets all the possible moves for a player.
    def get_player_moves(self, player):
        moves = []
        for x in xrange(GRID_WIDTH):
            for y in xrange(GRID_HEIGHT):
                unit = self.grid.get(x, y)
                # If the tile contains a unit.
                if unit:
                    # If the given player owns the unit.
                    if unit.owner == player:
                        # Add the possible moves from that unit to
                        # the player's possible moves.
                        moves += unit.get_moves([x, y], self)
        
        return moves


class Game(object):

    def __init__(self):
        # This will hold the actual units,
        # and will be used for logic.
        initial_grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        self.__populate_grid__(initial_grid)

        # This will be the initial state.
        self.state = State(initial_grid, 0)
        
        # Keep track of how many turn
        self.renderer = Renderer()

    # Generate a homerow of pieces.
    def __homerow__(self, owner, top=True):
        if top:
            y = GRID_HEIGHT - 1
            direction = -1   
        else:
            y = 0
            direction = 1

        row = [Rook(owner, direction), Knight(owner, direction), Bishop(owner, direction)]
        row += [Queen(owner, direction), King(owner, direction)]
        row += [Bishop(owner, direction), Knight(owner, direction), Rook(owner, direction)]
        
        return row

    # Populate a board with units in their default placement.
    def __populate_grid__(self, grid):
        # Bottom side of the board.
        grid.tiles[0] = self.__homerow__(PLAYER1, top=False)
        grid.tiles[1] = [Pawn(PLAYER1, 1) for i in range(GRID_WIDTH)]

        # Top side of the board.
        grid.tiles[GRID_HEIGHT - 1] = self.__homerow__(PLAYER2, top=True)
        grid.tiles[GRID_HEIGHT - 2] = [Pawn(PLAYER2, -1) for i in range(GRID_WIDTH)]


    def draw_state(self):
        self.renderer.render_state(self.state)

    # Gets a move from the player.
    def get_user_move(self, player):
        moveset = self.state.get_player_moves(player)
        coords = [m[:2] for m in moveset]
        #print moveset
        print '\nCommand format: <unit x><unit y> to <target x><target y>'
        valid = False
        
        while not valid:
            user_in = raw_input('Please enter your move: ')

            try:
                split_input = user_in.split(' to ')
                unit_x, unit_y = [split_input[0][0], split_input[0][1]]
                target_x, target_y = [split_input[1][0], split_input[1][1]]
                unit_x = string.ascii_lowercase.index(unit_x.lower())
                unit_y = int(unit_y) - 1
                target_x = string.ascii_lowercase.index(target_x.lower())
                target_y = int(target_y) - 1
            except:
                print "Sorry, I don't understand your coordinates."
                continue

            # Get the unit object.
            unit = self.state.grid.get(unit_x, unit_y)
            print unit
            
            # Make sure a unit exists in that tile.
            # And that it's owned by the player
            # currently making a move.
            if not unit or unit.owner != player:
                print "Sorry, you don't own that unit."                   
                continue

            else:
                # Make sure the target is a valid move.
                move = [[unit_x, unit_y], [target_x, target_y]]
                if move in coords:
                    # Return the appropriate move object.
                    return moveset[coords.index(move)]
                else:
                    print "Sorry, that isn't a valid move."
                    continue


    def execute(self, cur_state, move):
        origin, target, flag = move
        if flag:
            if flag['action'] == CASTLE:
                #self.castle(origin, target, flag['side'])
                print 'Castling not yet implmented.'
            elif flag['action'] == PROMOTION:
                print 'Promotion not yet implemented.'

        new_state = self.move(cur_state, origin, target)
        new_state.turn += 1

        return new_state


    def move(self, cur_state, origin, target):
        # Move and Unit Information
        ox, oy = origin
        tx, ty = target
        unit = cur_state.grid.get(ox, oy)
        target_unit = cur_state.grid.get(tx, ty)

        # Current State Information
        turn = cur_state.turn
        p1_caps = cur_state.p1_caps
        p2_caps = cur_state.p2_caps

        #Update that the unit has moved.
        if not unit.has_moved:
            unit.has_moved = True

        # If the target is a unit...
        if target_unit:
            # Record the capture.
            if unit.owner == PLAYER1:
                p1_caps.append(target_unit)
            else:
                p2_caps.append(target_unit)

        # Construct the new state where the unit is moved.
        # (Since in the event of a capture the captured unit
        #  will be overwritten in the grid, no special
        #  handling is required.)

        new_grid = copy(cur_state.grid)
        new_grid.set(unit, tx, ty)
        new_grid.set(None, ox, oy)

        return State(new_grid, turn, p1_caps, p2_caps)

    def advance_turn(self):
        if self.state.turn % 2 == 0:
            player = PLAYER1
        else:
            player = PLAYER2

        move = self.get_user_move(player)
        self.state = self.execute(self.state, move)
        self.draw_state()

    def play(self):
        self.draw_state()
        while True:
            self.advance_turn()

class Grid(object):

    def __init__(self, height, width):
        # Board dimensions.
        self.width = width
        self.height = height
        self.tiles = [
            [None for i in range(self.height)] for j in range(self.width)]

    # Access the board's grid.
    def get(self, x, y):
        return self.tiles[y][x]

    # Set a tile
    def set(self, val, x, y):
        self.tiles[y][x] = val


def main():
    g = Game()
    g.play()
    exit()

if __name__ == '__main__':
    main()
