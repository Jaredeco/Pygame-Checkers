import pygame
from pygame import gfxdraw

pygame.init()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
FPS = 60
CLOCK = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Checkers")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

black = (0, 0, 0)
white = (255, 255, 255)
red = (238, 59, 59)
green = (127, 255, 0)
blue = (0, 255, 255)


class Piece:
    def __init__(self, x, y, i, j, color):
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.color = color
        self.radius = (SCREEN_WIDTH / 8) / 3

    def draw(self):
        gfxdraw.filled_circle(win, int(self.x), int(self.y), int(self.radius), self.color)

    @staticmethod
    def _remove_highlight():
        BOARD.highlight_available()
        BOARD.av_pos = None

    @staticmethod
    def coor_from_pos(r, c):
        dim = 8
        x = BOARD.game[r][c].x + (SCREEN_WIDTH / dim) / 2
        y = BOARD.game[r][c].y + (SCREEN_WIDTH / dim) / 2
        return x, y

    def skipped(self, i, j):
        if abs(i - self.i) > 1 or abs(j - self.j) > 1:
            r = self.i + (i - self.i) + (-1 if i - self.i > 0 else 1)
            c = self.j + (j - self.j) + (-1 if j - self.j > 0 else 1)
            BOARD.game[r][c].piece = None
            av_pos = [(a, b) for a, b in BOARD.available_pos(i, j) if abs(a - i) > 1 or abs(b - j) > 1]
            if len(av_pos):
                BOARD.av_pos = [(i, j)] + av_pos
                BOARD.highlight_available()
            else:
                BOARD.change_turn()
        else:
            BOARD.change_turn()

    def move(self, i, j):
        if (i, j) in BOARD.av_pos and (i, j) != BOARD.av_pos[0]:
            self._remove_highlight()
            self.skipped(i, j)
            BOARD.game[self.i][self.j].piece = None
            x, y = self.coor_from_pos(i, j)
            self.x, self.y, self.i, self.j = x, y, i, j
            BOARD.game[i][j].piece = self

        else:
            self._remove_highlight()


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

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))
        if self.highlighted:
            pygame.draw.rect(win, green, (self.x + 1.5, self.y + 1.5, self.size - 1.5, self.size - 1.5), 3)
        if self.piece is not None:
            self.piece.draw()

    def highlight(self):
        if not self.highlighted:
            self.highlighted = True
        else:
            self.highlighted = False


class Board:
    def __init__(self):
        self.turn = red
        self.av_pos = None
        dim = 8
        self.size = SCREEN_WIDTH // dim
        self.game = [[] for i in range(dim)]
        for i in range(dim):
            for j in range(dim):
                pos = Position(self.size * j + 2, self.size * i + 2, i, j,
                               white if (not j % 2 and not i % 2) or (j % 2 and i % 2) else black, None)
                if (not i % 2 and j % 2 and (5 <= i or i <= 2)) or (i % 2 and not j % 2 and (5 <= i or i <= 2)):
                    pos.piece = Piece(pos.x + (SCREEN_WIDTH / dim) / 2, pos.y + (SCREEN_WIDTH / dim) / 2, i, j,
                                      blue if i <= 2 else red)
                self.game[i].append(pos)

    def draw(self):
        for i in range(len(self.game)):
            for j in range(len(self.game[0])):
                self.game[i][j].draw()

    def get_row_col_clicked(self, pos):
        row = pos[1] // self.size
        col = pos[0] // self.size
        return row, col

    @staticmethod
    def is_valid(i, j):
        if 0 <= i <= 7 and 0 <= j <= 7:
            return True
        return False

    def available_pos(self, i, j, idx=None):
        av_pos = [(i + 1, j + 1), (i + 1, j - 1), (i - 1, j + 1), (i - 1, j - 1)]
        av_pos = av_pos[:2] if self.turn == blue else av_pos[2:]
        if idx is not None:
            return av_pos[idx]
        pos = [(i, j)]
        for i, (r, c) in enumerate(av_pos):
            if self.is_valid(r, c):
                if self.game[r][c].piece is None:
                    pos.append((r, c))
                else:
                    rs, cs = self.available_pos(r, c, i)
                    if self.game[r][c].piece.color != self.turn and self.is_valid(rs, cs) and self.game[rs][
                        cs].piece is None:
                        pos.append((rs, cs))
        return pos

    def highlight_available(self):
        for i, j in self.av_pos:
            self.game[i][j].highlight()

    def select_move(self, r, c):
        if self.av_pos is None:
            piece = self.game[r][c].piece
            if piece is not None and piece.color == self.turn:
                av_pos = self.available_pos(r, c)
                self.av_pos = av_pos
                self.highlight_available()
        else:
            i, j = self.av_pos[0][0], self.av_pos[0][1]
            piece = self.game[i][j].piece
            piece.move(r, c)

    def change_turn(self):
        self.turn = blue if self.turn == red else red

    def winner(self):
        pass

    def reset(self):
        self.__init__()


def redraw_win():
    win.fill(blue if BOARD.turn == blue else red)
    BOARD.draw()
    pygame.display.flip()


# Todo:
#   -return positions until no skip
#   -king functionality
#   -maybe minimax
BOARD = Board()
RUN = True
while RUN:
    CLOCK.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            r, c = BOARD.get_row_col_clicked(event.pos)
            BOARD.select_move(r, c)
    redraw_win()
pygame.quit()
