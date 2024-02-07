import pygame
import random


class BlockGenerator(object):
    """
    class to provide the next block type to update the grid
    """
    def __init__(self):
        self.piece_types = ['long', 'mid', 'l_l', 'l_r', 'sq', 's_l', 's_r']
        self.coords = {
            'long': [(0, 0), (1, 0), (2, 0), (3, 0)],
            'mid': [(1, 1), (0, 1), (2, 1), (1, 0)],
            'l_l': [(1, 1), (0, 0), (0, 1), (2, 1)],
            'l_r': [(1, 1), (2, 0), (0, 1), (2, 1)],
            'sq': [(0, 0), (0, 1), (1, 0), (1, 1)],
            's_l': [(1, 1), (0, 0), (1, 0), (2, 1)],
            's_r': [(1, 1), (0, 1), (1, 0), (2, 0)],
        }

    # 4 types of tetris pieces
    # ####,    #    #      #  ##  ##     ##
    #         ### , ###, ###, ##,  ## , ##

    def generate(self):
        """ represent each piece as a list of 4 coordinate offsets """
        cur_piece = random.choice(self.piece_types)
        return Piece(type=cur_piece, coord=self.coords[cur_piece])


class Piece(object):
    def __init__(self, type, coord):
        self.type = type
        self.coord = coord
