import random

from music21.stream import Stream, Measure, Part, Score, Opus
from music21.meter import TimeSignature


class Form(object):
    def __init__(self, duration, score):
        self.duration = duration

        self.bar_durs = []
        total = 0
        while total < self.duration:
            dur = self.choose_bar_duration()
            self.bar_durs.append(dur)
            total = total + dur * 4

    def choose_bar_duration(self):
        return random.randint(2, 7)


def make(score):
    form = score.form.movement_2

    previous_dur = None
    for part in score.Parts.list:
        for dur in form.bar_durs:
            for n in range(4):
                measure = Measure()
                if n == 0 and dur != previous_dur:
                    measure.timeSignature = TimeSignature('{}/4'.format(dur))
                part.append(measure)
            previous_dur = dur

