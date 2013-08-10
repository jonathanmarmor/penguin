import random


def scale(x, minimum, maximum, floor=0, ceiling=1):
    return ((ceiling - floor) * (float(x) - minimum))/(maximum - minimum) + floor


def weighted_choice(options, weights):
    rand = random.random()
    rand = scale(rand, 0, 1, 0, sum(weights))
    total = 0
    for i, weight in enumerate(weights):
        total += weight
        if rand < total:
            return options[i]


def fibonacci(n):
    a, b = 0, 1
    for x in range(n):
        a, b = b, a + b
    return a


GOLDEN_MEAN = float(fibonacci(30)) / fibonacci(31)


def divide(dur, units):
    """Divide the length `dur` into `units` sections"""
    if units > dur:
        return "hey, you can't divide `dur` into a number of units greater than `dur`"
    divs = []
    while len(divs) < units - 1:
        r = random.randint(1, dur - 1)
        if r not in divs:
            divs.append(r)
    divs.sort()
    divs.append(dur)
    result = []
    prev = 0
    for d in divs:
        unit = d - prev
        result.append(unit)
        prev = d
    return result


def frange(x, y, step=1.0):
    while x < y:
        yield x
        x += step