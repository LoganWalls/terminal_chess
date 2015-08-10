import string


class Renderer(object):
    
    def __init__(self):
        pass

    def render_state(self, state):
        self.render_UI(state)
        self.render_grid(state.grid)

    def render_UI(self, state):
        p1 = 'SAFE'
        p2 = 'SAFE'

        c1 = ' '.join([u.sprite for u in state.p1_caps])
        c2 = ' '.join([u.sprite for u in state.p2_caps])

        if state.p1_check:
            p1 = 'CHECK'
        if state.p2_check:
            p2 = 'CHECK'

        print 'Player 1:\n', '\tCaptures:\t', c1,'\n',
        print '\t King:\t',p1
        print 'Player 2:\n', '\tCaptures:\t', c2,'\n',
        print '\t King:\t', p2,'\n'

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

