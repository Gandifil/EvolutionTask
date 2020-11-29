from copy import deepcopy


class Evolution(object):
    """docstring"""

    def __init__(self, count, f):
        """Constructor"""
        self.pool = [f() for _ in range(count)]
        self.points = []
        print('Создано начальное поколение количеством в {} штук.'.format(count))

    def selectionIf(self, f):
        oldCount = len(self.pool)
        self.pool = [value for value in self.pool if f(value)]
        print('Произведена селекция. Было {}, стало {}.'.format(oldCount, len(self.pool)))

    def selectionByFitness(self, f):
        oldCount = len(self.pool)
        self.pool = [self.pool[i] for i in range(len(self.pool)) if f(self.points[i])]
        print('Произведена селекция по значению функции приспособленности. Было {}, стало {}.'.format(oldCount, len(self.pool)))

    def mutate(self):
        for x in self.pool:
            x.mutate()
        self.points = []
        print('Выполнены мутации')

    def budding(self, k):
        newPool = []
        for item in self.pool:
            for _ in range(k):
                newPool.append(deepcopy(item))
        print('Произведено почкование. Было {}, стало {}.'.format(len(self.pool), len(newPool)))
        self.pool = newPool

    def fitness(self):
        self.points = [value.fitness() for value in self.pool]
        return self.points

    def getBest(self):
        self.fitness()
        index = self.points.index(max(self.points))
        return self.pool[index]