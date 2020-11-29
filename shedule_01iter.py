import sheduling
from itertools import *

cellsCount = 6 * 2 * len(sheduling.times)
lessons1 = sheduling.lessons1 + [None for _ in range(cellsCount - len(sheduling.lessons1))]
lessons2 = sheduling.lessons2 + [None for _ in range(cellsCount - len(sheduling.lessons2))]

maxFitness = -1000000000
theBestShedule = None

i = 0
for lessonIndexes1 in permutations(lessons1):
    for lessonIndexes2 in permutations(lessons2):
        print("Check ", i)
        i += 1

        shedule = sheduling.GlobalShedule()
        shedule.for247 = sheduling.Shedule()
        shedule.for247.fillConcreteWithRandom(lessonIndexes2)
        shedule.for248 = sheduling.Shedule()
        shedule.for248.fillConcreteWithRandom(lessonIndexes1)

        if shedule.isValid():
            fitness = shedule.fitness()
            if fitness > maxFitness:
                print(shedule)
                print(fitness)
                theBestShedule = shedule
                maxFitness = fitness

print(theBestShedule)
print(theBestShedule.fitness())