"""A piece of music for Dedalus ensemble.

http://www.youtube.com/watch?v=_syDjTX90zA&feature=share&list=PL477C973BF13F8BBE

"""

import datetime
import random
import math

import music21


class Gesture(music21.stream.Stream):
    pass


class GesturePart(music21.stream.Stream):
    pass


class Phrase(music21.stream.Stream):
    pass


class PhrasePart(music21.stream.Stream):
    pass


def get_score():
    score = music21.stream.Score()

    md = music21.metadata.Metadata()
    md.title = 'Penguin Atlas of African History'
    md.composer = 'Jonathan Marmor'
    md.date = datetime.datetime.utcnow().strftime('%Y/%m/%d')
    md.groupTitle = 'Dedalus'
    md.dedication = 'Didier Aschour'
    score.insert(0, md)

    fl = music21.instrument.Piccolo()
    fl.nickname = 'fl'
    sax = music21.instrument.SopranoSaxophone()
    sax.nickname = 'sax'
    vla = music21.instrument.Viola()
    vla.nickname = 'viola'
    vc = music21.instrument.Violoncello()
    vc.nickname = 'cello'
    tbn = music21.instrument.Trombone()
    tbn.nickname = 'tbn'
    gtr = music21.instrument.ElectricGuitar()
    gtr.nickname = 'gtr'

    score.inst_list = [fl, sax, vla, vc, tbn, gtr]

    score.instruments = {}
    score.parts_by_inst = {}
    score.instruments_by_name = {}
    score.parts_list = []
    for i in score.inst_list:
        abbr = i.instrumentAbbreviation
        score.instruments_by_name[i.nickname] = i
        part = music21.stream.Part()
        part.insert(0, i)
        part.id = abbr
        score.insert(0, part)
        score.parts_list.append(part)
        score.instruments[abbr] = i
        score.instruments[i.nickname] = i
        score.parts_by_inst[abbr] = part
        score.parts_by_inst[i.nickname] = part

    score.insert(0, music21.layout.StaffGroup(score.parts_list))

    return score


def scale(x, minimum, maximum, floor=0, ceiling=1):
    return ((ceiling - floor) * (float(x) - minimum))/(maximum - minimum) + floor


class Penguin(object):
    def __init__(self):
        self.piece_duration = self.choose_piece_duration()
        self.choose_major_sections(self.piece_duration)

    def choose_piece_duration(self):
        # Choose the total number of beats in the piece
        self.num_beats = random.randint(450, 550)
        return self.num_beats

    def choose_major_sections(self, piece_num_beats):
        """Choose the durations of the two major sections of the piece.

        Choose a split point between the golden mean of the whole piece and
        the golden mean of the section between the golden mean of the piece and
        the end of the piece."""

        # Golden mean
        minimum = 377.0 / 610

        # The golden mean of the section between the golden mean and 1
        maximum = scale(minimum, 0, 1, minimum, 1)

        # Pick a random float between minimum and maximum
        division = scale(random.random(), 0, 1, minimum, maximum)

        # Get the durations of each section
        section1_num_beats = int(scale(division, 0, 1, 0, piece_num_beats))
        section2_num_beats = piece_num_beats - section1_num_beats

        self.section1 = Section1(self, section1_num_beats)
        self.section2 = Section2(self, section2_num_beats)

    def report_percentage_of_num_beats(self, n):
        return round(scale(n, 0, self.num_beats), 2)

    def report_num_beats(self):
        return {
            'piece.num_beats': self.num_beats,
            'section1': {
                'num_beats': self.section1.num_beats,
                'coverage': self.report_percentage_of_num_beats(self.section1.num_beats)
            },
            'section2': {
                'num_beats': self.section2.num_beats,
                'coverage': self.report_percentage_of_num_beats(self.section2.num_beats)
            }
        }


class Section1(object):
    def __init__(self, piece, num_beats):
        self.piece = piece
        self.num_beats = num_beats





class Section2(object):
    def __init__(self, piece, num_beats):
        self.piece = piece
        self.num_beats = num_beats


def run():
    penguin = Penguin()
    return penguin


if __name__ == '__main__':
    run()
