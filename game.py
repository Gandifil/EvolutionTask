from enum import Enum

class Command(Enum):
    empty = 1
    black = 2
    white = 3

class Checker(object):
    """docstring"""

    def __init__(self, command, is):
        """Constructor"""
        self.command = command
        self.type =
        pass

class Cell(object):
    """docstring"""

    def __init__(self, command = Command.empty):
        self.command = command
        pass

class Board(object):
    """docstring"""

    def __init__(self):
        self.cells = [[Cell() for _ in range(8)] for _ in range(8)]
        pass

    def fill(self):
        for x in range(8):
            for y in range(8):
                if x + y % 2 == 1:
                    if y < 3:
                        self.cells[x][y] = Cell(Command.black)
                    if y > 4:
                        self.cells[x][y] = Cell(Command.white)


    def __str__(self):
        result = ""
        for x in range(8):
            result += str(self.cells)