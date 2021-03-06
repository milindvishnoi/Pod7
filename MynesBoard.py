# Board Constructor and manipulator for Mynes

from typing import List
from MyneSquare import MyneSquare
import random
import pygame

ICON_SIZE = 24

class MynesBoard:
    """
    === Public Attributes ===
    board (List[List[MyneSquare]]]):  Matrix representation of the board state, to be used by Mynes

    === Private Attributes ===
    # _width (int): board width (right)
    # _height (int): board height (down)
    # _mine_count (int): number of mines placed on the board
    # _mine_lst (List[Tuple(int, int)]): stores where mines are placed on the board
    """

    def __init__(self, mode: str):
        """
        Create a base board for Mynes. Default values for width, height, and mine count.
        (0,0) is the top-left of the board.
        """
        num_of_blocks, num_of_bombs = self.create_board(mode)
        # Board size in playable spaces
        self.width, self.height = num_of_blocks, num_of_blocks
        self.mine_count = num_of_bombs
        # Construct board of empty squares
        self.board = [[
            MyneSquare(0, False, "Icons/temp_empty.png",
                       pygame.Rect(x * ICON_SIZE, y * ICON_SIZE,
                                   ICON_SIZE, ICON_SIZE))
            for y in range(self.height)] for x in range(self.width)]
        self.mine_lst = []
        self.place_mine()
        for x in range(self.width):
            for y in range(self.height):
                self.place_numbers(x, y)

    def create_board(self, mode)-> int:
        """Return the """
        if mode == "Easy":
            return (10, 10)
        elif mode == "Medium":
            return (20, 50)
        else:
            return (30, 100)

    def place_mine(self) -> None:
        """
        Place mines randomly on the squares and store coordinates in self.mine_lst
        """
        i = 0
        while i < self.mine_count:
            mine_x, mine_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            # Prevent duplicate mines
            if self.board[mine_y][mine_x].value != -1:
                self.board[mine_y][mine_x].value = -1
                i += 1
                self.mine_lst.append([mine_y, mine_x])

    def place_numbers(self, x: int, y: int) -> None:
        """
        Detects mine and updates the surrounding squares
        """
        bombs_surrounded = 0
        if self.board[x][y].value == -1:
            surroundings = [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1],
                            [x+1,y-1],[x+1,y],[x+1,y+1]]
            for pos in surroundings:
                if self.inbound(pos[0], pos[1]):
                    if self.board[pos[0]][pos[1]].value != -1:
                        self.board[pos[0]][pos[1]].value += 1
                        bombs_surrounded += 1
        return bombs_surrounded

    def inbound(self, x: int, y: int) -> bool:
        """
        Used to check if the square exists inside the game board or not
        :param x: height
        :param y: width
        :return: true if in the game board else false
        """
        if (y < self.width and y >= 0) and (x >= 0 and x < self.height):
            return True
        return False
