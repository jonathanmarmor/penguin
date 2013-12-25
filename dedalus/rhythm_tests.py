import sys

from music21.note import Note, Rest
from music21.pitch import Pitch
from music21.stream import Stream, Measure, Part, Score, Opus
from music21.meter import TimeSignature, MeterSequence, MeterTerminal
from music21.duration import Duration
from music21.spanner import Glissando, Slur
from music21.metadata import Metadata
from music21.instrument import (Piccolo, SopranoSaxophone, Viola, Violoncello,
    Trombone, ElectricGuitar)
from music21.layout import StaffGroup

from utils import split_at_beats, join_quarters

"""
Rhythm notation criteria
-



"""


#### 1


def bar1():
    notes = []
    # Eighth rest, eighth tied to half tied to eighth, eighth rest
    r1 = Rest()
    r1.duration = Duration(0.5)
    notes.append(r1)

    n1 = Note()
    n1.duration = Duration(3.0)
    notes.append(n1)

    r2 = Rest()
    r2.duration = Duration(0.5)
    notes.append(r2)
    return notes


def test_1():
    score = Score()
    bars = [bar1]
    for bar in bars:
        notes = bar()
        measure = notate_measure(notes)
        score.append(measure)
    score.show()


def notate_measure(notes):
    ts = TimeSignature('4/4')
    # ts.beatSequence.partition(4)
    # print ts.beatSequence

    ts.beamSequence.partition(4)
    # print ts.beamSequence

    m = Measure()
    m.timeSignature = ts
    [m.append(n) for n in notes]

    # m.sliceByBeat(inPlace=True)

    m.makeBeams()
    return m


#### 2


def fix_durations(notes):
    durations = [note['duration'] for note in notes]

    components_list_split = split_at_beats(durations)

    components_list_joined = [join_quarters(note_components) for note_components in components_list_split]

    for note, components in zip(notes, components_list_joined):
        note['durations'] = components

    return notes


def bar2():
    durations = [.75, .5, 1.25, .75, .75]
    notes = [{'duration': d} for d in durations]
    notes = fix_durations(notes)
    return notes


def notate_notes(notes):
    ts = TimeSignature('4/4')
    # ts.beatSequence.partition(4)
    # print ts.beatSequence

    ts.beamSequence.partition(4)
    # print ts.beamSequence

    m = Measure()
    m.timeSignature = ts

    for note in notes:
        n = Note()
        d = Duration()
        d.fill(note['durations'])
        n.duration = d
        m.append(n)

    m.makeBeams()
    return m


def test_beams():
    score = Score()
    bars = [bar2]
    for bar in bars:
        notes = bar()
        measure = notate_notes(notes)
        score.append(measure)
    return score





if __name__ == '__main__':
    print
    score = test_beams()
    if 'noshow' not in sys.argv:
        score.show()