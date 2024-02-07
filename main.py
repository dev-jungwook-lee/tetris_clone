import pygame as pg
import yaml

from game.grid import Grid
from game.block import BlockGenerator

from game.utils import *


def main(cfg):
    run = True
    pg.init()
    win = pg.display.set_mode((cfg.display.width, cfg.display.height))
    pg.display.set_caption("Tetris Clone")
    clock = pg.time.Clock()

    # init
    cur_grid = Grid(cfg.grid)
    block_gen = BlockGenerator()
    generate_new = True
    key_hold = None

    # stack
    # what do we want to do? until the press up is detected
    # we would like the motion to continue in that direction
    key_stack = []
    cur_dir = None

    # game loop
    while run:
        # sets the fps for the game
        clock.tick(cfg.fps)

        # catch event for end of run
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            # get keystrokes to update piece
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    if "right" in key_stack:
                        key_stack.remove("right")
                    cur_dir = "right"
                    key_stack.append(cur_dir)
                elif event.key == pg.K_LEFT:
                    if "left" in key_stack:
                        key_stack.remove("left")
                    cur_dir = "left"
                    key_stack.append(cur_dir)
                elif event.key == pg.K_UP:
                    cur_grid.rotate()
                elif event.key == pg.K_SPACE:
                    generate_new = True
                elif event.key == pg.K_q:
                    run = False

            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    if "right" in key_stack:
                        key_stack.remove("right")
                    if key_stack:
                        cur_dir = key_stack[-1]
                    else:
                        cur_dir = None
                if event.key == pg.K_LEFT:
                    if "left" in key_stack:
                        key_stack.remove("left")
                    if key_stack:
                        cur_dir = key_stack[-1]
                    else:
                        cur_dir = None

        # peek for the direction and execute
        if cur_dir:
            cur_grid.move(direction=cur_dir)


        # retrieve next block
        if generate_new:
            cur_piece = block_gen.generate()
            cur_grid.add(cur_piece)
            generate_new = False

        cur_grid.draw(win)
        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    game_cfg = get_cfg("config.yaml")
    main(game_cfg)
