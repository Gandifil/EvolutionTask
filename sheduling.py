import random

rooms = [64, 307, 308, 309, 310, 318, 204, 409, 415, 325, 402]
times = ["8:20-9:50",
         "10:00-11:35",
         "12:05-13:40",
         "13:50-15:25",
         "15:35-17:10",
         "17:20-18:40",
         "18:45-20:05"]

dayStrings = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

teachers = ["Сидоров С. П.", "Блинков Ю. А.", "Иванилова С. В.", "Сосновская А. А.", "Позднева С. П.",
            "Шевырев С. П.", "Балаш В.А.", "Файзлиев А. Р."]

lessons1 = [
    "пр. Спецкурс 9.1 Сидоров С. П.",
    "пр. Спецкурс 9.1 Сидоров С. П.",
    "лек. Спецкурс 3 Блинков Ю. А.",
    "пр. Спецкурс 3 Блинков Ю. А.",
    "пр. Научно-исследовательская работа Сидоров С. П.",
    "пр. Научно-исследовательская работа Сидоров С. П.",
    "лек. Спецкурс 10.1 Иванилова С. В.",
    "лек. Спецкурс 10.1 Иванилова С. В.",
    "пр. Спецкурс 10.1 Иванилова С. В.",
    "пр. Спецкурс 10.1 Иванилова С. В.",
    "пр. Иностранный язык Сосновская А. А.",
    "пр. Философские проблемы науки и техники Позднева С. П.",
    "лек. Эволюционное моделирование и алгоритмы Шевырев С. П.",
    "пр. Эволюционное моделирование и алгоритмы Шевырев С. П.",
    "лек. Спецкурс 9.1 Сидоров С. П.",
    "лек. Спецкурс 9.1 Сидоров С. П."]

lessons2 = [
    "пр. Научно-исследовательская работа Шевырев С. П.",
    "пр. Научно-исследовательская работа Шевырев С. П.",
    "пр. Спецкурс 3 Блинков Ю. А.",
    "пр. Спецкурс 3 Блинков Ю. А.",
    "лек. Спецкурс 3 Блинков Ю. А.",
    "пр. Эволюционное моделирование и алгоритмы Шевырев С. П.",
    "пр. Эволюционное моделирование и алгоритмы Шевырев С. П.",
    "пр. Научно-исследовательская работа Балаш В.А.",
    "пр. Научно-исследовательская работа Балаш В.А.",
    "пр. Спецкурс 9.1 Файзлиев А. Р.",
    "пр. Спецкурс 10.1 Иванилова С. В.",
    "лек. Спецкурс 10.1 Иванилова С. В.",
    "лек. Спецкурс 10.1 Иванилова С. В.",
    "пр. Иностранный язык Сосновская А. А.",
    "пр. Философские проблемы науки и техники Позднева С. П.",
    "лек. Эволюционное моделирование и алгоритмы Шевырев С. П.",
    "лек. Спецкурс 9.1 Сидоров С. П.",
    "лек. Спецкурс 9.1 Сидоров С. П.",
    "пр. Спецкурс 9.1 Файзлиев А. Р.",
    "пр. Спецкурс 10.1 Иванилова С. В.", ]

def getBreaks(bools):
    changes = 0
    last = False
    for isSet in bools:
        if isSet is not last:
            changes += 1
        last = isSet
    if last:
        changes += 1

    breaks = (changes - 2) / 2
    return breaks if breaks > 0 else 0


class Shedule(object):
    """Класс расписания для конкретной группы"""

    def __init__(self):
        """Constructor"""
        self.cells = [[None for _ in range(len(times))] for _ in range(6 * 2)]

    def getRandomCellIf(self, f):
        """Возвращает индексы случайной ячейки, подходящей требованиям f"""
        while True:
            day = random.randint(0, len(self.cells) - 1)
            time = random.randint(0, len(times) - 1)
            if f(self.cells[day][time]):
                break
        return day, time

    def fillx(self, lesson, room):
        """Находит случайным образом свободную ячейку и выписывает туда дисциплину и аудиторию"""
        day, time = self.getRandomCellIf(lambda x: x is None)
        self.cells[day][time] = [lesson, room]

    def fill(self, lessons):
        """Заполняет расписание списком дисциплин. Аудитория проставляется случайным образом"""
        for lesson in lessons:
            self.fillx(lesson, random.choice(rooms))

    def fillConcreteWithRandom(self, lessons):
        """Заполняет расписание списком дисциплин. Аудитория проставляется случайным образом"""
        i = 0
        for day in range(6 * 2):
            for time in range(len(times)):
                lesson = lessons[i]
                if lesson is not None:
                    self.cells[day][time] = (lesson, random.randint(0, 10000000))
                else:
                    self.cells[day][time] = None
                i += 1


    def __str__(self):
        result = ""
        result += "Знаменатель:\n"
        for day in range(6 * 2):
            if day == 6:
                result += "Числитель:\n"
            result += "\t" + dayStrings[day % 6] + "\n"
            for time in range(len(times)):
                if not self.cells[day][time] is None:
                    result += "\t\t" + times[time] + " --- "
                    room = str(self.cells[day][time][1])
                    result += self.cells[day][time][0] + " Ауд. " + room
                    result += '\n'
        return result

    def isValid(self):
        """Правильная ли структура"""
        return True

    def mutate(self):
        """Мутирует объект. В данном случае: или меняем аудиторию в
        случайной ячейке, или перемещаем конкретную пару"""
        mutationType = random.randint(0, 1)
        day, time = self.getRandomCellIf(lambda x: x is not None)

        if mutationType == 1:
            self.cells[day][time][1] = random.randint(0, len(rooms) - 1)

        if mutationType == 0:
            buffer = self.cells[day][time]
            self.cells[day][time] = None
            self.fillx(buffer[0], buffer[1])

    def fitness(self):
        """Функция приспособленности"""
        result = 0
        for day in range(6 * 2):
            usedTime = [x is not None for x in self.cells[day]]

            if any(usedTime):
                result -= 100
                if day == 5:
                    result -= 200

            for time in range(len(times)):
                if usedTime[time]:
                    if time == 0 or time == len(times) - 1:
                        result -= 100
                    if time == 1 or time == len(times) - 2:
                        result -= 50

            # проверяем "окна" в расписании
            result -= getBreaks(usedTime) * 200

        return result

    def has(self, day, time, str):
        cell = self.cells[day][time]
        return cell is not None and cell[0].find(str) >= 0

    def fillFromList(self, lessons, lessonsIndexes, roomsIndexes):
        for i in range(len(lessons)):
            day = lessonsIndexes[i] / len(time)
            time = lessonsIndexes[i] % len(time)
            rooms = roomsIndexes[i]
            self.cells[day][time] = (lessons[i], rooms)


class GlobalShedule(object):
    """docstring"""

    def __init__(self):
        self.for248 = Shedule()
        self.for247 = Shedule()

    def fill(self):
        self.for248.fill(lessons1)
        self.for247.fill(lessons2)

    def isValid(self):
        """Аудитория на должна использоватся в одно и тоже время разными преподавателями"""
        for day in range(6 * 2):
            for time in range(len(times)):
                fcell = self.for248.cells[day][time]
                scell = self.for247.cells[day][time]
                if fcell is not None and scell is not None:
                    equalRooms = fcell[1] == scell[1]
                    equalLesson = fcell[0] == scell[0]
                    if equalRooms and not equalLesson:
                        return False
                    if equalLesson and not equalRooms:
                        return False

        return self.for248.isValid() and self.for247.isValid()

    def __str__(self):
        result = "Группа 247\n"
        result += self.for247.__str__()

        result += "Группа 248\n"
        result += self.for248.__str__()

        return result

    def mutate(self):
        """Мутирует объект. Для этого вызываем мутации у всех включенных расписаний"""
        self.for248.mutate()
        self.for247.mutate()

    def fitness(self):
        """Функция приспособленности"""
        result = 0
        for day in range(6 * 2):
            for time in range(len(times)):
                fcell = self.for248.cells[day][time]
                scell = self.for247.cells[day][time]
                if fcell is not None and scell is not None:
                    if fcell[0] == scell[0] and fcell[1] == scell[1]:
                        result += 200

        for teacher in teachers:
            for day in range(6 * 2):
                usedTime = [self.for248.has(day, i, teacher) or self.for247.has(day, i, teacher) for i in range(len(times))]

                if any(usedTime):
                    result -= 200

                result -= getBreaks(usedTime) * 200


        return self.for248.fitness() + self.for247.fitness() + result
