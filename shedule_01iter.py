import signal
import sys
from math import factorial

import sheduling
from itertools import *

cellsCount = 6 * 2 * len(sheduling.times)


def convert(lessonsPrint, indexes):
    assert len(lessonsPrint) == len(indexes)
    lessons = [None for _ in range(cellsCount)]
    for i in range(len(lessonsPrint)):
        lessons[indexes[i]] = lessonsPrint[i]
    shedule = sheduling.Shedule()
    shedule.fillConcreteWithRandom(lessons)
    return shedule


maxFitness = -1000000000
theBestShedule = None

i = 0


def permCount(n, m):
    return factorial(n) / factorial(n - m)


def save():
    with open('result.txt', 'w') as f:
        print(theBestShedule, file=f)
        print(theBestShedule.fitness(), file=f)


shedule = sheduling.GlobalShedule()
length1 = permCount(cellsCount, len(sheduling.lessons1))
length2 = permCount(cellsCount, len(sheduling.lessons2))
length = int(length1 * length2)

for lessonIndexes1 in permutations(range(cellsCount), len(sheduling.lessons1)):
    for lessonIndexes2 in permutations(range(cellsCount - 1, -1, -1), len(sheduling.lessons2)):
        # print("Iter ", i)
        i += 1
        shedule.for248 = convert(sheduling.lessons1, lessonIndexes1)
        shedule.for247 = convert(sheduling.lessons2, lessonIndexes2)

        if shedule.isValid():
            fitness = shedule.fitness()
            print("Check ", i, "/", length, " shedule with fitness ", fitness)
            if fitness > maxFitness:
                print("New best shedule!")
                theBestShedule = shedule
                maxFitness = fitness
                save()

print(theBestShedule)
print(theBestShedule.fitness())
