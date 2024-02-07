import pygame

from game.block import BlockGenerator


class Grid(object):
    """ todo
    1. try drawing the playing area [done]
    """
    def __init__(self, grid_cfg):
        self.w = grid_cfg.width
        self.h = grid_cfg.height
        self.c = grid_cfg.cell
        self.x = grid_cfg.x
        self.y = grid_cfg.y
        self.border_offset = grid_cfg.border_offset
        self.start = grid_cfg.start

        # initialize state grid (w x h)
        self.grid_ = [[0 for _ in range(self.h)] for _ in range(self.w)]
        self.cur_piece = None
        self.cur_type = None

        self.rot_cnt = 0

    def add(self, piece):
        piece.coord = [[out[0] + self.start[0], out[1] + self.start[1]] for out in piece.coord]
        self.cur_piece = piece

    def _draw_grid(self, win):
        win.fill((0, 0, 0))

        # draw a background border
        border_rect = (self.x - self.border_offset,
                       self.y - self.border_offset,
                       self.w * self.c + 2 * self.border_offset,
                       self.h * self.c + 2 * self.border_offset)
        pygame.draw.rect(win, (200, 200, 200), border_rect, 2)

        # draw the playing area and populated grids
        for i in range(self.w):
            for j in range(self.h):
                # calculate width
                cur_w = (i * self.c)
                cur_h = (j * self.c)
                cur_rect = (cur_w + self.x, cur_h + self.y, self.c, self.c)
                pygame.draw.rect(win, (200, 200, 200), cur_rect, 1)

        # draw the current piece
        for coord in self.cur_piece.coord:
            cur_w = (coord[0] * self.c)
            cur_h = (coord[1] * self.c)
            cur_rect = (cur_w + self.x, cur_h + self.y, self.c, self.c)
            pygame.draw.rect(win, (200, 200, 200), cur_rect)
        # rects are (x, y, width, height)

    def draw(self, win):
        self._draw_grid(win)

    def move(self, direction):
        # check if the piece is already at most right
        edge_test = False
        for coord in self.cur_piece.coord:
            if direction == "right":
                edge_test |= coord[0] >= self.w - 1
            else:
                edge_test |= coord[0] <= 0

        if not edge_test:
            for i in range(len(self.cur_piece.coord)):
                if direction == "right":
                    self.cur_piece.coord[i][0] += 1
                else:
                    self.cur_piece.coord[i][0] -= 1

    def rotate(self):
        if self.cur_piece.type == 'sq':
            return

        # simple rotate swap axis
        if self.cur_piece.type != 'long':
            pivot_x, pivot_y = self.cur_piece.coord[0]
        else:
            pivot_x, pivot_y = self.cur_piece.coord[1]

        rot = [[1, 0], [0, 1], [-1, 0], [0, -1],]
        for coord in self.cur_piece.coord:
            # rotation matrix is [cos x, -sin x; sin x, -cos x] ccw
            # 90 deg is pi/2 which is [0, -1; 1, 0]
            coord[0], coord[1] = coord[0] - pivot_x, coord[1] - pivot_y
            coord[0], coord[1] = -coord[1], coord[0]
            coord[0] += pivot_x
            coord[1] += pivot_y

            if self.cur_piece.type == "long":
                coord[0] += rot[self.rot_cnt][0]
                coord[1] += rot[self.rot_cnt][1]

        self.rot_cnt = (self.rot_cnt + 1) % 4

        # make sure to not go beyond the max
        left_offset = 0
        for coord in self.cur_piece.coord:
            left_offset = min(left_offset, coord[0] - 0)
        if left_offset < 0:
            for coord in self.cur_piece.coord:
                coord[0] += -left_offset

        right_offset = 0
        for coord in self.cur_piece.coord:
            right_offset = max(right_offset, coord[0] - (self.w - 1))
        if right_offset > 0:
            for coord in self.cur_piece.coord:
                coord[0] -= right_offset

        top_offset = 0
        for coord in self.cur_piece.coord:
            top_offset = min(top_offset, coord[1] - 0)
        if top_offset < 0:
            for coord in self.cur_piece.coord:
                coord[1] += -top_offset

    def __repr__(self):
        return self.grid_.__repr__()
