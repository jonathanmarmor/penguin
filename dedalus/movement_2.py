import random
from copy import deepcopy

from music21.stream import Measure
from music21.meter import TimeSignature
from music21.duration import Duration
from music21.note import Note, Rest

from utils import divide


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


def choose_notes(dur_to_fill):
    """Picks the material for an """
    play = random.randint(0, 5) > 0  # 5 out of 6 will play a note
    if play:
        durs = divide(dur_to_fill * 4, 3)
        durs = [d / 4.0 for d in durs]

        r1 = Rest()
        r1.duration = Duration(durs[0])
        n = Note()
        n.duration = Duration(durs[1])
        r2 = Rest()
        r2.duration = Duration(durs[2])
        return [r1, n, r2]
    else:
        r = Rest()
        r.duration = Duration(dur_to_fill)
        return [r]






def make(score):
    form = score.form.movement_2

    previous_dur = None
    for dur in form.bar_durs:

        for part in score.Parts.list:

            notation = choose_notes(dur)

            for n in range(4):
                measure = Measure()
                if n == 0 and dur != previous_dur:
                    measure.timeSignature = TimeSignature('{}/4'.format(dur))
                part.append(measure)

                notation_copy = deepcopy(notation)

                for note in notation_copy:
                    measure.append(note)

        previous_dur = dur


"""
TODO:
- map out instrument ranges
- for each instrument, identify the range shared with each other instrument
- make a phrase:
    - pick the number of notes
    - for each note
        - generate the rhythm (choose_notes(bar_duration))
        - pick an instrument to play it
        - remove that instrument from the pool of available instruments for the first two repetitions of the phrase
        - pick another instrument with a shared range to hand the note to for the second two repetitions
        - remove the second instrument from the pool of available instruments for the second two repetitions of the phrase
        - pick a pitch for the note from the shared range
    - resulting data should look like:
    {
        'couplet_1': {
            'inst1': {
                'rhythm': [1, 6, 2],
                'pitch': 'F4'
            },
            'inst2': {
                'rhythm': [9],
                'pitch': 'r'
            },
            ...
        },
        'couplet_2': {
            ...
        }
    }
    - for each instrument, for each phrase (4 of them), instantiate measures, instantiate notes, append to measures

"""
