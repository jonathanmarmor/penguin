import datetime
import random
import math

from music21.note import Note
from music21.pitch import Pitch
from music21.stream import Stream, Measure, Part, Score, Opus
from music21.duration import Duration
from music21.spanner import Glissando, Slur
from music21.metadata import Metadata
from music21.instrument import (Piccolo, SopranoSaxophone, Viola, Violoncello,
    Trombone, ElectricGuitar)
from music21.layout import StaffGroup

from utils import GOLDEN_MEAN, scale, weighted_choice
import movement_2


class Instruments(object):
    names = ['fl', 'sax', 'vla', 'vc', 'tbn', 'gtr']
    fl = Piccolo()
    sax = SopranoSaxophone()
    vla = Viola()
    vc = Violoncello()
    tbn = Trombone()
    gtr = ElectricGuitar()
    list = [fl, sax, vla, vc, tbn, gtr]
    dict = {}
    for name, inst in zip(names, list):
        inst.nickname = name
        dict[name] = inst


class Parts(object):
    names = ['fl', 'sax', 'vla', 'vc', 'tbn', 'gtr']
    fl = Part()
    sax = Part()
    vla = Part()
    vc = Part()
    tbn = Part()
    gtr = Part()
    list = [fl, sax, vla, vc, tbn, gtr]
    dict = {}
    for name, part, inst in zip(names, list, Instruments.list):
        part.id = name
        dict[name] = part
        part.insert(0, inst)


def get_metadata(timestamp, movement_number=None, movement_name=None):
    md = Metadata()
    md.title = 'Penguin Atlas of African History'
    md.composer = 'Jonathan Marmor'
    md.date = timestamp.strftime('%Y/%m/%d')
    md.groupTitle = 'Dedalus'
    md.dedication = 'Didier Aschour'
    if movement_number:
        md.movementNumber = movement_number
    if movement_name:
        md.movementName = movement_name
    return md


class Form(object):
    def __init__(self, score):
        self.score = score
        self.choose_piece_duration()
        self.make_movements()
        self.choose_when_quarter_tones_start()

    def choose_piece_duration(self):
        """Choose the total number of beats in the piece"""
        self.piece_duration = random.randint(450, 550)  # 7.5 - a little more than 9 minutes

    def make_movements(self):
        one, two = self.choose_movement_durations()
        # self.movement_1 = movement_1.Form(one, self.score)
        self.movement_2 = movement_2.Form(two, self.score)

    def choose_movement_durations(self):
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
        one = int(scale(division, 0, 1, 0, self.piece_duration))
        two = self.piece_duration - one
        return one, two

    def choose_when_quarter_tones_start(self):
        # somewhere between 2 and 4 minutes in
        self.quarter_tones_start = scale(random.random(), 0, 1, 60 * 2, 60 * 4)


def make():
    score = Score()
    score.Parts = Parts
    score.Instruments = Instruments
    score.form = Form(score)

    timestamp = datetime.datetime.utcnow()
    score.insert(0, get_metadata(timestamp))

    [score.insert(0, part) for part in Parts.list]
    score.insert(0, StaffGroup(Parts.list))

    # form
    # notes/details

    # mv1 = movement_1.make(score)
    movement_2.make(score)

    score.show()

    return score


if __name__ == '__main__':
    make()
