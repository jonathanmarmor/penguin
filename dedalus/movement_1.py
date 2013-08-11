import random

from music21.note import Note, Rest
from music21.pitch import Pitch
from music21.stream import Stream, Measure
from music21.meter import TimeSignature
from music21.duration import Duration
from music21.spanner import Glissando, Slur

from utils import GOLDEN_MEAN, scale, frange, weighted_choice
import song_forms


class Song(object):
    def __init__(self, number, piece, movement):
        self.number = number
        self.piece = piece
        self.movement = movement

        instrument_opts = piece.instruments.names[:]

        form = song_forms.choose()

        self.type = 'solo'
        if number % 2:
            self.type = 'ensemble'

        if self.type == 'solo':
            solo_ensemble_hash = random.choice(movement.solo_ensemble_options.keys())
            soloists = movement.solo_ensemble_options[solo_ensemble_hash]['instruments']
            solo_ensemble_names = [s.nickname for s in soloists]
            solo_ensemble_shared_notes = movement.solo_ensemble_options[solo_ensemble_hash]['notes']
            # Remove chosen ensemble from options
            del movement.solo_ensemble_options[solo_ensemble_hash]

            # remove chosen soloists from instrument options for the song
            for soloist in solo_ensemble_names:
                instrument_opts.remove(soloist)
            self.accompanists = [piece.i.d[name] for name in instrument_opts]

        else:
            # who plays, who sits out?
            ensemble_size = weighted_choice([3, 4, 5, 6], [1, 4, 5, 4])
            ensemble_names = random.sample(instrument_opts, ensemble_size)
            self.ensemble = [piece.i.d[name] for name in ensemble_names]

        phrase_types = []
        for segment_type in set(form):
            if segment_type == 0:
                phrase_type = VerseType()
            if segment_type == 1:
                phrase_type = ChorusType()
            if segment_type == 2:
                phrase_type = BridgeType()
            if segment_type == 3:
                phrase_type = BreakdownType()
            if segment_type == 4:
                # TODO is this used?
                phrase_type = FurtherBreakdownType()

            phrase_types.append(phrase_type)

        for segment in form:
            phrase = phrase_types[segment].make_phrase()


class VerseType(object):
    pass

class ChorusType(object):
    pass

class BridgeType(object):
    pass

class BreakdownType(object):
    pass

class FurtherBreakdownType(object):
    pass


class Movement1(object):
    def __init__(self, duration, piece):
        self.duration = duration
        self.songs = []
        self.solo_ensemble_options = piece.i.get_unison_ensembles(min_notes=6)

        total = 0
        n = 0
        while total < duration:
            song = Song(n, piece, self)
            self.songs.append(song)
            total += song.duration
            n += 1
