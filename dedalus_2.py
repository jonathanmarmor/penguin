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
    # piece duration
    # movement durations
    # movement 1 form
        # alternating sections: solo and ensemble
        # starting a little earlier than halfway through, alternating quarter tones and 12 to the octave (to keep it simple, just do one solo/ensemble pair in quarter tones, then one pair not)
        # each section is some kind of aabaccba kind of thing
        # each unit (eg a, b, c) is a bar
        # the last minute the density should go way down, maybe by slowing the tempo and removing notes randomly
    # movement 2 form
        # totally random long sustained tones?
        # pick durations and offsets, then pick pitches so that simultanaeties are consonant, or something
        # there need to be silences too
        # maybe make long measures (6/4 to 20/4?) and pick rest-note-rest durations for each instrument
        # maybe repeat each one twice with different instrumentation each time? or avoid repetition?
    pass


def main():
    score = Score()

    timestamp = datetime.datetime.utcnow()
    score.insert(0, get_metadata(timestamp))

    [score.insert(0, part) for part in Parts.list]
    score.insert(0, StaffGroup(Parts.list))

    # form
    # notes/details

    score.show()

    return score


if __name__ == '__main__':
    main()
