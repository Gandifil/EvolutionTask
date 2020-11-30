from copy import deepcopy
from enum import Enum
import random
from evolution import Evolution


class Command(Enum):
    nothing = 0
    empty = 1
    black = 2
    white = 3


class Cell(object):
    """Клетка поля. Может быть с шашкой (разных команд), пустой, или за пределами поля"""

    def __init__(self, command=Command.empty):
        self.command = command
        pass

    def isEmpty(self):
        return self.command == Command.empty

    def isFriend(self, c):
        return c == self.command

    def isFoe(self, c):
        foe = Command.white if c == Command.black else Command.black
        return foe == self.command

    def set(self, c):
        self.command = c

    def destroy(self):
        self.command = Command.empty


class Board(object):
    """Доска"""

    def __init__(self):
        self.cells = [[Cell() for _ in range(8)] for _ in range(8)]
        pass

    def fill(self):
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 1:
                    if y < 3:
                        self.cells[x][y] = Cell(Command.black)
                    if y > 4:
                        self.cells[x][y] = Cell(Command.white)

    def __str__(self):
        result = ""
        for y in range(8):
            for x in range(8):
                if self.cells[x][y].command == Command.empty:
                    result += '-'
                if self.cells[x][y].command == Command.white:
                    result += 'w'
                if self.cells[x][y].command == Command.black:
                    result += 'b'
            result += '\n'
        return result

    def get(self, x, y):
        r = range(8)
        return self.cells[x][y] if x in r and y in r else Cell(Command.nothing)

    def move(self, x, y, ax, ay):
        result = deepcopy(self)
        result.cells[ax][ay].set(result.cells[x][y].command)
        result.cells[x][y].destroy()
        return result

    def attack(self, x, y, ax, ay):
        result = deepcopy(self)
        result.cells[ax][ay].set(result.cells[x][y].command)

        dx = ax - x
        dx = int(dx / abs(dx))
        dy = ay - y
        dy = int(dy / abs(dy))
        for i in [1]:
            result.cells[x + i * dx][y + i * dy].destroy()

        result.cells[x][y].destroy()
        return result

    def getAllMoves(self, command):
        results = []
        for y in range(8):
            for x in range(8):
                cell = self.get(x, y)
                if cell.isFriend(command):
                    shift = -1 if command == Command.white else 1
                    if self.get(x - 1, y + shift).isEmpty():
                        results.append(self.move(x, y, x - 1, y + shift))
                    if self.get(x + 1, y + shift).isEmpty():
                        results.append(self.move(x, y, x + 1, y + shift))
                    if self.get(x - 1, y + shift).isFoe(command) and self.get(x - 2, y + 2 * shift).isEmpty():
                        results.append(self.attack(x, y, x - 2, y + 2 * shift))
                    if self.get(x + 1, y + shift).isFoe(command) and self.get(x + 2, y + 2 * shift).isEmpty():
                        results.append(self.attack(x, y, x + 2, y + 2 * shift))
        return results


class GameStrategy:

    def __init__(self):
        self.friendL = [[0 for _ in range(8)] for _ in range(8)]
        self.foeL = [[0 for _ in range(8)] for _ in range(8)]

    def fill(self):
        for y in range(8):
            for x in range(8):
                self.friendL[x][y] = random.choice([-1, 0, 1])
                self.foeL[x][y] = random.choice([-1, 0, 1])

    def fitness(self, board, command):
        result = 0
        for y in range(8):
            for x in range(8):
                cell = board.cells[x][y]
                if cell.isFriend(command):
                    result += self.friendL[x][y]
                if cell.isFoe(command):
                    result += self.foeL[x][y]
        return result

    def isValid(self):
        """Правильная ли структура"""
        return True

    def mutate(self):
        """Мутирует объект. В данном случае: или меняем аудиторию в
        случайной ячейке, или перемещаем конкретную пару"""
        for y in range(8):
            for x in range(8):
                self.friendL[x][y] += random.randrange(-2, 3)
                self.foeL[x][y] += random.randrange(-2, 3)

    def __str__(self):
        result = str(self.friendL) + '\n'
        result += str(self.foeL)
        return result


def fight(a, b, isPrint=False):
    """Проводим бой между двумя стратегиями. Первая а - белые, вторая b -черные.
    Если нету вариантов шагов - проигрыш. Если шагов больше 100 -ничья
    Начисление очков: проигрыш - -1, победа - 1, ничья - 0 каждой стороне."""
    board = Board()
    board.fill()

    current = Command.white
    for i in range(100):
        strategy = a if current == Command.white else b
        variants = board.getAllMoves(current)

        if len(variants) == 0:
            return (-1, 1) if current == Command.white else (1, -1)

        used = max(variants, key=lambda v: strategy.fitness(v, current))
        board = used
        if isPrint:
            print(board)
        current = Command.white if current == Command.black else Command.black

    return 0, 0


def generate():
    strategy = GameStrategy()
    strategy.fill()
    return strategy


def tournament(strategies):
    """Турнир. Получаем список стратегий, проводим бой каждой с каждой. Очки полученные из функции fight
    прибавляем к итоговой таблице очков. Таблицу возвращаем"""
    results = [0 for _ in strategies]
    for a in range(len(strategies)):
        for b in range(a + 1, len(strategies)):
            ac, bc = fight(strategies[a], strategies[b])
            results[a] += ac
            results[b] += bc
    return results


def test():
    strategy1 = GameStrategy()
    strategy1.fill()
    strategy2 = GameStrategy()
    strategy2.fill()
    print(fight(strategy1, strategy2, True))


def genetic():
    evolution = Evolution(1, generate)
    generationCount = 10
    for generation in range(generationCount):
        print("Поколение {}".format(generation + 1))
        evolution.budding(10)
        evolution.mutate()

        # проводим турнир
        evolution.points = tournament(evolution.pool)
        print(evolution.points)
        # самая большая оценка за турнир
        mark = max(evolution.points)
        # оставляем только те, что участвуют в турнире
        evolution.selectionByFitness(lambda fitness: fitness == mark)
        print("\n")

    print("Лучший представитель")
    theBest = evolution.pool[0]
    print(theBest)
    evolution = Evolution(10, generate)
    print(tournament([theBest, *evolution.pool]))


# test()
genetic()
