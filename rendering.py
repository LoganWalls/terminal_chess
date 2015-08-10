import string


class Renderer(object):
    
    def __init__(self):
        pass

    def render_state(self, state):
        self.render_grid(state.grid)

    def render_grid(self, grid):
        tiles = grid.tiles
        line = '   ' + ('-' * (grid.width * 4)) + '-'
        buff = [line]

        for i, row in enumerate(tiles):
            tmp = str(i + 1) + '  | '
            tmp += ' | '.join([u.sprite if u else ' ' for u in row]) + ' |' 
            buff.append(tmp)
            buff.append(line)

        # Add bottom indexing.
        buff.append('     ' + '   '.join(list(string.ascii_uppercase)[:grid.width]))
        buff.reverse()
        buff = ' \n'.join(buff)
        print buff

