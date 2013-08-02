"""

- Choose durations of major sections

- how long until quarter tones start?

- alternating-ish between solo melody with accompaniment and ensemble music
    - solo could be several instruments in rhythmic unison
    - (S = solo, E = ensemble) mostly SESESESE, but sometimes SSE with two different soloists




- second endings are great: abac
- second beginnings are great: abcb
"""

import random
import string
from collections import Counter
import itertools


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


def validate(array):
    # Remove boring ones
    len_uniques = len(set(array))
    if len_uniques < 2:
        return False
    # Remove overly interesting ones
    if len_uniques > 4:
        return False
    # Remove illegal ones
    for index, item in enumerate(array[1:]):
        if item not in array[:index + 1] and item - 1 not in array[:index + 1]:
            return False
    return True


def get_forms(n):
    args = [range(i + 1) for i in range(n)]
    product = itertools.product(*args)
    return filter(validate, product)


# Outdated
def choose_next(things):
    if len(things) == 0:
        return 1
    uniques = set(things)
    options = list(uniques) + [max(uniques) + 1]
    weights = ([1] * len(uniques)) + [len(uniques)]
    return weighted_choice(options, weights)
    # return random.choice(range(1, len(uniques) + 2))


def make(n):
    make_more_things = True
    things = []
    while make_more_things:
        next = choose_next(things)
        things.append(next)
        make_more_things = len(things) < n
    return ''.join([string.letters[t - 1] for t in things])


def count():
    d = {}
    for n in range(2, 12):
        d[n] = Counter({})
        for x in range(10000):
            d[n][make(n)] += 1
    return d

