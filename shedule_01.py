import evolution
import sheduling
import random
import statistics


def generate():
    shedule = sheduling.GlobalShedule()
    shedule.fill()
    return shedule


evolution = evolution.Evolution(5, generate)
generationCount = 30
for generation in range(generationCount):
    print("Поколение {}".format(generation + 1))
    evolution.budding(10)
    evolution.mutate()
    evolution.selectionIf(lambda x: x.isValid())
    while len(evolution.pool) > 1000:
        points = evolution.fitness()
        median = statistics.median(points)
        if not evolution.selectionByFitness(lambda fitness: fitness >= median):
            evolution.selectionIf(lambda x: random.choice([True, False]))

    print("\n")

print("Лучший представитель")
print(evolution.getBest())
print(evolution.getBest().fitness())
