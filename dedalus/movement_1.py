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
            self.solo_ensemble_shared_notes = movement.solo_ensemble_options[solo_ensemble_hash]['notes']
            # Remove chosen ensemble from options
            del movement.solo_ensemble_options[solo_ensemble_hash]

            # remove chosen soloists from instrument options for the song
            for soloist in solo_ensemble_names:
                instrument_opts.remove(soloist)
            self.accompanists = [piece.i.d[name] for name in instrument_opts]
            # TODO not everyone should accompany.  Some should sit out.

        else:
            # who plays, who sits out?
            ensemble_size = weighted_choice([3, 4, 5, 6], [1, 4, 5, 4])
            ensemble_names = random.sample(instrument_opts, ensemble_size)
            self.ensemble = [piece.i.d[name] for name in ensemble_names]


        # make a phrase for each unique part of the form (eg, an `a` in `abacabac`)
        unique_phrases = []
        for f in set(form):
            if self.type == 'solo':
                unique_phrases.append(SoloPhrase())
            elif self.type == 'ensemble':
                unique_phrases.append(EnsemblePhrase())

        # Copy the phrases in the order specified by form
        phrases = []
        for f in form:
            phrases.append(unique_phrases[f])

        # TODO render phrases into music21 objects


class Phrase(object):
    """
    - instruments can have one of two types of material: solo or accompaniment
    - solo has more notes, ornaments, and is less tied to the meter
    - accomp has very simple rhythms that outline the meter, no ornaments, and generally longer duration notes
    - if song.type is solo:
        - the soloist group all play a solo part in unison
        - all the remaining instruments play accompaniment parts. maybe some in rhythmic unison?
    - if song.type is ensemble:
        - everyone plays a different solo part


    once we have all the rhythms (and maybe contours?) then use the harmony validator from movement 2 to choose the pitches
    pitch options should be within a small range of the previous note, perhaps with the smallest intervals preferred

    """

    def __init__(self):
        pass

    def copy(self):
        pass

    def make_solo(self):
        """used by both SoloPhrase and EnsemblePhrase"""
        pass


class SoloPhrase(Phrase):
    def make_accompaniment(self):
        pass


class EnsemblePhrase(Phrase):
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
