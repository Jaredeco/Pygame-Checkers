import pygame
from pygame import gfxdraw
from checkers.constants import CROWN, SCREEN_WIDTH, blue, red, green


class Position:
    def __init__(self, x, y, i, j, color, piece):
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.color = color
        self.piece = piece
        self.size = SCREEN_WIDTH / 8
        self.highlighted = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))
        if self.highlighted:
            pygame.draw.rect(win, green, (self.x + 1.5, self.y + 1.5, self.size - 1.5, self.size - 1.5), 3)
        if self.piece is not None:
            self.piece.draw(win)

    def highlight(self):
        if not self.highlighted:
            self.highlighted = True
        else:
            self.highlighted = False


class Piece:
    def __init__(self, x, y, i, j, color):
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.color = color
        self.radius = int((SCREEN_WIDTH / 8) / 3)
        self.is_king = False

    def draw(self, win):
        if self.is_king:
            gfxdraw.filled_circle(win, int(self.x), int(self.y), self.radius, self.color)
            win.blit(CROWN, (self.x - self.radius + 0.9, self.y - self.radius + 3.5))
        else:
            gfxdraw.filled_circle(win, int(self.x), int(self.y), self.radius, self.color)

    @staticmethod
    def _remove_highlight(board):
        board.highlight_available()
        board.av_pos = None

    @staticmethod
    def coor_from_pos(board, r, c):
        dim = 8
        x = board.game[r][c].x + (SCREEN_WIDTH / dim) / 2
        y = board.game[r][c].y + (SCREEN_WIDTH / dim) / 2
        return x, y

    def skipped(self, board, i, j):
        if abs(i - self.i) > 1 or abs(j - self.j) > 1:
            r = self.i + (i - self.i) + (-1 if i - self.i > 0 else 1)
            c = self.j + (j - self.j) + (-1 if j - self.j > 0 else 1)
            board.game[r][c].piece = None
            av_pos = [(a, b) for a, b in board.available_pos(i, j) if abs(a - i) > 1 or abs(b - j) > 1]
            if len(av_pos):
                board.skipping = True
                board.av_pos = [(i, j)] + av_pos
                board.highlight_available()
            else:
                board.change_turn()
        else:
            board.change_turn()

    def king(self, i):
        if (self.color == red and i == 0) or (self.color == blue and i == 7):
            self.is_king = True

    def move(self, board, i, j):
        if (i, j) in board.av_pos and (i, j) != board.av_pos[0]:
            self._remove_highlight(board)
            self.skipped(board, i, j)
            board.game[self.i][self.j].piece = None
            x, y = self.coor_from_pos(board, i, j)
            self.x, self.y, self.i, self.j = x, y, i, j
            board.game[i][j].piece = self
            self.king(i)
        else:
            if not board.skipping:
                self._remove_highlight(board)
