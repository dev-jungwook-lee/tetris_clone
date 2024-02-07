import pygame
import yaml

from game.grid import Grid
from game.block import BlockGenerator

from game.utils import *


def main(cfg):
    run = True
    pygame.init()
    win = pygame.display.set_mode((cfg.display.width, cfg.display.height))
    pygame.display.set_caption("Tetris Clone")
    clock = pygame.time.Clock()

    # init
    cur_grid = Grid(cfg.grid)
    block_gen = BlockGenerator()
    generate_new = True
    key_hold = None

    # game loop
    while run:
        # sets the fps for the game
        clock.tick(cfg.fps)

        # catch event for end of run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # get keystrokes to update piece
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                cur_grid.move(direction="right")
            elif keys[pygame.K_LEFT]:
                cur_grid.move(direction="left")
            elif keys[pygame.K_UP]:
                cur_grid.rotate()
            elif keys[pygame.K_SPACE]:
                generate_new = True
            elif keys[pygame.K_q]:
                run = False

        # retrieve next block
        if generate_new:
            cur_piece = block_gen.generate()
            cur_grid.add(cur_piece)
            generate_new = False

        cur_grid.draw(win)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game_cfg = get_cfg("config.yaml")
    main(game_cfg)
