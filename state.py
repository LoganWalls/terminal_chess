from constant_defs import *
from copy import copy
class State(object):

    def __init__(self, grid, turn, p1_caps=[], p2_caps=[], sim_depth=0):
        # Game information.
        self.grid = grid

        # Units each player has captured.
        self.p1_caps = p1_caps
        self.p2_caps = p2_caps

        # The number of turns which have passed.
        self.turn = turn
        self.sim_depth = sim_depth

        # Determine if either player is in check.
        self.p1_check = self.__player_check__(PLAYER1)
        self.p2_check = self.__player_check__(PLAYER2)

    # Check if the given position is in danger.
    def check_position(self, pos, opponent):
        opponent_moves = self.get_player_moves(opponent)
        
        for m in opponent_moves:
            origin, target, flag = m
            # If taking the King is a valid move for
            # the opponent...
            if target == pos:
                return True

        return False

    # Returns whether or not the given player is in check
    # in this state.
    def __player_check__(self, player):
        if player == PLAYER1:
            opponent = PLAYER2
        else:
            opponent = PLAYER1

        king_pos = self.__get_king__(player)

        return self.check_position(king_pos, opponent)


    # Return the coordinates of the king
    # belonging to 'player'.
    def __get_king__(self, player):
        for x in xrange(GRID_WIDTH):
            for y in xrange(GRID_HEIGHT):
                cur_tile = self.grid.get(x, y)
                if type(cur_tile).__name__ == 'King':
                    if cur_tile.owner == player:
                        return [x, y]
        # Raise an error if we don't find a king after searching the board.
        raise RuntimeError('No king found for player: '+str(player))



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
                if unit is not None:
                    # If the given player owns the unit.
                    if unit.owner == player:
                        # Add the possible moves from that unit to
                        # the player's possible moves.
                        moves += unit.get_moves([x, y], self, sim_depth=self.sim_depth)
        
        return moves

    def simulate_move(self, origin, target):
        ox, oy = origin
        tx, ty = target
        unit = self.grid.get(ox, oy)
        new_grid = copy(self.grid)
        new_grid.set(unit, tx, ty)
        new_grid.set(None, ox, oy)
        sim_depth = self.sim_depth + 1

        return State(new_grid, 0, sim_depth=sim_depth)

    def leads_to_check(self, origin, target, player):
        sim = self.simulate_move(origin, target)
        check = sim.in_check(player)
        print check
        return check


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