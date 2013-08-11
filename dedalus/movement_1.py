import random

from music21.note import Note, Rest
from music21.pitch import Pitch
from music21.stream import Stream, Measure
from music21.meter import TimeSignature
from music21.duration import Duration
from music21.spanner import Glissando, Slur

from utils import GOLDEN_MEAN, scale, frange
import song_forms


class Song(object):
    def __init__(self, number, piece, movement):
        self.number = number
        self.piece = piece
        self.movement = movement

        form = song_forms.choose()

        self.type = 'solo'
        if number % 2:
            self.type = 'ensemble'
        # solo or ensemble
            # solo
                # soloist ensemble (in unison)
                # accompaniment ensemble
            # ensemble
                # who plays, who sits out?

        for segment in form:
            if segment == 0:
                phrase = Verse()
            if segment == 1:
                phrase = Chorus()
            if segment == 2:
                phrase = Bridge()
            if segment == 3:
                phrase = Breakdown()
            if segment == 4:
                # TODO is this used?
                phrase = FurtherBreakdown()


class Verse(object):
    pass

class Chorus(object):
    pass

class Bridge(object):
    pass

class Breakdown(object):
    pass

class FurtherBreakdown(object):
    pass


class Movement1(object):
    def __init__(self, duration, piece):
        self.duration = duration
        self.songs = []

        total = 0
        n = 0
        while total < duration:
            song = Song(piece, self, n)
            self.songs.append(song)
            total += song.duration
            n += 1
