"""
# Major section 1
    - alternating between accompanied solos and ensemble sections?
    - 2 to 4 minutes in, suddenly it's ok to also use quarter tones, and they are equally likely as any other notes

## Solo sections

## Ensemble sections
    - everybody has their own part
    - parts are just dropped on top of each other?  but simultaneous harmonies are consonant and each invidual lick has reasonable voice leading


# Major section 2
    - starts between golden mean of the total piece duration and golden mean of the section between that and the end of the piece
    - similar to the rest of piece, but thinner in texture, fewer notes (randomly removed?), slower, and more spacious
    - is there internal structure in major section 2?  I don't think so.
    - Need to make it transparent, like it's grinding to a halt.
    - still use quarter tones?  why not.
    - maybe add some lush isolated sustained chords

"""


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


def choose_piece_duration():
    """Choose the total number of beats in the piece"""
    return random.randint(450, 550)  # 7.5 - a little more than 9 minutes


def choose_major_sections_durations(piece_duration):
    """Choose the durations of the two major sections of the piece.

    Choose a split point between the golden mean of the whole piece and
    the golden mean of the section between the golden mean of the piece and
    the end of the piece."""

    minimum = GOLDEN_MEAN

    # The golden mean of the section between the golden mean and 1
    maximum = scale(minimum, 0, 1, minimum, 1)

    # Pick a random float between minimum and maximum
    division = scale(random.random(), 0, 1, minimum, maximum)

    # Get the durations of each section
    section1_duration = int(scale(division, 0, 1, 0, piece_duration))
    section2_duration = piece_duration - section1_duration

    return section1_duration, section2_duration


def when_quarter_tones_start():
    # somewhere between 2 and 4 minutes in
    return scale(random.random(), 0, 1, 60 * 2, 60 * 4)


def make_form():
    piece_duration = choose_piece_duration()
    section1_duration, section2_duration = choose_major_sections_durations(piece_duration)
    qt_start = when_quarter_tones_start()
