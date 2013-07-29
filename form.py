import random
import string
from collections import Counter


def choose_next(things):
    if len(things) == 0:
        return 1
    uniques = set(things)
    return random.choice(range(1, len(uniques) + 2))


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


"""

# rules/preferences
# - second endings are great: abac
# - second beginnings are great: abcb

a
ab
aab
aba
abb
abc
aaab
aaba
abaa
aabb
abab
abba
abbb
aabc
abac
abca
abbc
abcb
abcc

aaaab
aaaba
aabaa
abaaa
aaabb
aabab
aabba
abaab
ababa
abbaa
aabbb
ababb
abbab
abbba
abbbb
aaabc
aabac
abaac
aabca
abaca
abcaa



...


faves:

abac
abcb

aaba
abaa
aabb

abab
abba




"""



