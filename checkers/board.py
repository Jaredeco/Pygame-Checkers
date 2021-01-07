from checkers.globals import SCREEN_WIDTH, black, white, brown, light_brown
from checkers.components import Position, Piece


class Board:
    def __init__(self):
        self.turn = black
        self.av_pos = None
        self.winner = None
        dim = 8
        self.skipping = False
        self.size = SCREEN_WIDTH // dim
        self.game = [[] for i in range(dim)]
        for i in range(dim):
            for j in range(dim):
                pos = Position(self.size * j+2, self.size * i+2, i, j,
                               light_brown if (not j % 2 and not i % 2) or (j % 2 and i % 2) else brown, None)
                if (not i % 2 and j % 2 and (5 <= i or i <= 2)) or (i % 2 and not j % 2 and (5 <= i or i <= 2)):
                    pos.piece = Piece(pos.x + (SCREEN_WIDTH / dim / 2), pos.y + (SCREEN_WIDTH / dim) / 2, i, j,
                                      white if i <= 2 else black)
                self.game[i].append(pos)

    def draw(self, win):
        for i in range(len(self.game)):
            for j in range(len(self.game[0])):
                self.game[i][j].draw(win)

    def get_row_col_clicked(self, pos):
        row = pos[1] // self.size
        col = pos[0] // self.size
        return row, col

    @staticmethod
    def is_valid(i, j):
        if 0 <= i <= 7 and 0 <= j <= 7:
            return True
        return False

    def available_pos(self, i, j, idx=None, is_king=None):
        if is_king is None:
            is_king = self.game[i][j].piece.is_king
        av_pos = [(i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1), (i - 1, j - 1)]
        if not is_king:
            av_pos = av_pos[:2] if self.turn == white else av_pos[2:]
        if idx is not None:
            return av_pos[idx]
        pos = [(i, j)]
        for i, (r, c) in enumerate(av_pos):
            if self.is_valid(r, c):
                if self.game[r][c].piece is None:
                    pos.append((r, c))
                else:
                    rs, cs = self.available_pos(r, c, i, is_king)
                    if self.game[r][c].piece.color != self.turn and self.is_valid(rs, cs) and self.game[rs][
                        cs].piece is None:
                        pos.append((rs, cs))
        return pos

    def highlight_available(self):
        for i, j in self.av_pos:
            self.game[i][j].highlight()

    def select_move(self, r, c):
        if not self.is_valid(r, c):
            return
        if self.av_pos is None:
            piece = self.game[r][c].piece
            if piece is not None and piece.color == self.turn:
                av_pos = self.available_pos(r, c)
                self.av_pos = av_pos
                self.highlight_available()
        else:
            i, j = self.av_pos[0][0], self.av_pos[0][1]
            piece = self.game[i][j].piece
            piece.move(self, r, c)

    def change_turn(self):
        self.skipping = False
        self.turn = white if self.turn == black else black

    def is_winner(self):
        for i in range(len(self.game)):
            for j in range(len(self.game[0])):
                piece = self.game[i][j].piece
                if piece is not None:
                    av_pos = self.available_pos(i, j)
                    if len(av_pos) > 1 and piece.color == self.turn:
                        return
        self.winner = black if self.turn == white else white

    def restart(self):
        self.__init__()
