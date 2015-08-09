import string
from units import *
from rendering import Renderer
from copy import deepcopy

class Game(object):

    def __init__(self):
        self.players = [Player('P1', 1), Player('P2', -1)]
        self.board = ChessBoard()
        self.board.populate(self.players[0], self.players[1])
        self.turn_count = 0

        self.renderer = Renderer()

    def draw_board(self):
        self.renderer.render_grid(self.board.get_grid())

    # Gets a move from the player.
    def get_user_move(self, player):
        possible_moves = self.board.get_player_moves(player)
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
            unit = self.board.grid.get(unit_x, unit_y)
            
            # Make sure a unit exists in that tile.
            # And that it's owned by the player
            # currently making a move.
            if not unit or unit.owner != player:
                print "Sorry, you don't own that unit."                   
                continue

            else:
                # Make sure the target is a valid move.
                move = [[target_x, target_y], unit]
                if move in possible_moves:
                    return move
                else:
                    print "Sorry, that isn't a valid move."
                    continue
    
    def execute_move(self, move):
        target, unit = move
        
        # Handle the actions in order of precedence.
        actions = sorted(unit.move_actions(target, self.board.grid))

        for a in actions:
            if a == SWAP:
                pass
            
            elif a == CAPTURE:
                other = self.get(target[0], target[1])
                # Record the capture.
                unit.owner.add_capture(other)
                # Delete the other unit.
                other.owner.remove_unit(other)
            
            elif a == MOVE:
                pass

            elif a == PROMOTE:
                pass

            # Update the board.
            self.board.execute(unit, target, a)

        # Update the unit's position.
        unit.update_position(target)

        #Update that the unit has moved.
        if not unit.has_moved:
            unit.has_moved = True


    def turn(self):
        if self.turn_count % 2 == 0:
            player = self.players[0]
        else:
            player = self.players[1]

        move = self.get_user_move(player)
        self.execute_move(move)
        self.draw_board()
        self.turn_count += 1

    def play(self):
        self.draw_board()
        while True:
            self.turn()

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

class ChessBoard(object):

    def __init__(self, width=8, height=8):
        
        # This will hold the actual units,
        # and will be used for logic.
        self.grid = Grid(width, height)

    # Generate a homerow of pieces.
    def __homerow__(self, owner, top=True):
        if top:
            y = self.grid.height - 1    
        else:
            y = 0

        row = [Rook(owner, 0, y), Knight(owner, 1, y), Bishop(owner, 2, y)]
        row += [Queen(owner, 3, y), King(owner, 4, y)]
        row += [Bishop(owner, 5, y), Knight(owner, 6, y), Rook(owner, 7, y)]
        
        return row

    def populate(self, player_one, player_two):
        self.grid.tiles[0] = self.__homerow__(player_one, top=False)
        self.grid.tiles[1] = [Pawn(player_one, i, 1) for i in range(self.grid.width)]
        self.grid.tiles[self.grid.height - 1] = self.__homerow__(player_two, top=True)
        self.grid.tiles[self.grid.height - 2] = [Pawn(player_two, i, self.grid.height - 2) for i in range(self.grid.width)]

    # Return the whole grid.
    def get_grid(self):
        return self.grid

    # Gets all the possible moves for a player.
    def get_player_moves(self, player, grid=None):
        moves = []
        if grid is None:
            grid = self.grid
        for row in grid.tiles:
            for tile in row:
                # If the tile contains a unit.
                if tile:
                    unit = tile
                    # If the given player owns the unit.
                    if unit.owner == player:
                        # Add the possible moves from that unit to
                        # the player's possible moves.
                        moves += [[m, unit] for m in unit.get_moves(self.get_grid())]
        
        return moves

    def execute(self, unit, target, action, grid=None):
            if grid is None:
                grid = self.grid

            if action == SWAP:
                self.swap(unit, target, grid)
            
            elif action == CAPTURE:
                self.capture(unit, target, grid)
            
            elif action == MOVE:
                self.move(unit, target, grid)

            elif action == PROMOTE:
                pass

    def swap(self, unit, target, grid):
        ux = unit.x
        uy = unit.y

        other = grid.get(target[0], target[1])
        other.update_position([ux, uy])

        grid.set(unit, target[0], target[1])
        grid.set(other, ux, uy)

    def move(self, unit, target, grid):
        ux = unit.x
        uy = unit.y
        grid.set(unit, target[0], target[1])
        grid.set(None, ux, uy)

    def capture(self, unit, target, grid):
        grid.set(None, target[0], target[1])

    def promote(self, old_unit, new_unit_type):
        ux = old_unit.x
        uy = old_unit.y
        old_unit.owner.remove_unit(old_unit)

        # Add the new unit.
        new_unit = new_unit_type(old_unit.owner, ux, uy)
        grid.set(new_unit, ux, uy)

    def leads_to_check(self, move):
        target, unit = move
        # A hypothetical grid.
        hyp_grid = deepcopy(self.grid)
        action = unit.move_actions()
        

class Player(object):

    def __init__(self, player_name, direction):
        self.p_name = player_name

        # This player's active units.
        self.units = []
        
        # Units this player has captured.
        self.captures = []

        # The direction this player is facing.
        self.direction = direction

    def add_capture(self, unit):
        self.captures.append(unit)

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        self.units.remove(unit)


def main():
    g = Game()
    g.play()
    exit()

if __name__ == '__main__':
    main()
