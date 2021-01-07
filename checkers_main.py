import pygame
from checkers.globals import SCREEN_WIDTH, SCREEN_HEIGHT, ICON,  black, white, green
from checkers.board import Board
from time import sleep
pygame.init()
pygame.font.init()
FPS = 60
CLOCK = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Checkers")
pygame.display.set_icon(ICON)
FONT = pygame.font.SysFont(None, 60)
BOARD = Board()


def redraw_win(winner):
    if winner is None:
        win.fill(white if BOARD.turn == white else black)
        BOARD.draw(win)
    else:
        win.fill(winner)
        text = "Black player won!" if winner == black else "White player won!"
        winner_text = FONT.render(text, True, green)
        win.blit(winner_text, winner_text.get_rect(center=win.get_rect().center))
        pygame.display.flip()
        sleep(3)
        BOARD.restart()
    pygame.display.flip()


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
                BOARD.is_winner()
        redraw_win(BOARD.winner)
    pygame.quit()


if __name__ == "__main__":
    main()
