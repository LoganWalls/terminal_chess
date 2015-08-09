import string


class Renderer(object):
    
    def __init__(self):
        pass

    def render_board(self, board):
        grid = board.get_grid()
        line = '   ' + ('-' * (board.width * 4)) + '-'
        buff = [line]

        for i, row in enumerate(grid):
            tmp = str(i + 1) + '  | '
            tmp += ' | '.join([u.sprite if u else ' ' for u in row]) + ' |' 
            buff.append(tmp)
            buff.append(line)

        # Add bottom indexing.
        buff.append('     ' + '   '.join(list(string.ascii_uppercase)[:board.width]))
        buff.reverse()
        buff = ' \n'.join(buff)
        print buff

