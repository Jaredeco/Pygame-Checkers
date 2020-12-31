import pygame
from checkers.constants import SCREEN_WIDTH, SCREEN_HEIGHT, ICON, blue, red
from checkers.board import Board

pygame.init()
FPS = 60
CLOCK = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("checkers")
pygame.display.set_icon(ICON)
BOARD = Board()


def redraw_win():
    win.fill(blue if BOARD.turn == blue else red)
    BOARD.draw(win)
    pygame.display.flip()


# Todo:
#   -king functionality
#   -maybe minimax
def main():
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


if __name__ == "__main__":
    main()
