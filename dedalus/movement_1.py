import random

from music21.note import Note, Rest
from music21.pitch import Pitch
from music21.stream import Stream, Measure
from music21.meter import TimeSignature
from music21.duration import Duration
from music21.spanner import Glissando, Slur

from utils import weighted_choice
import song_forms


class Song(object):
    def __init__(self, number, piece, movement):
        self.number = number
        self.piece = piece
        self.movement = movement

        instrument_opts = piece.instruments.names[:]

        form = self.form = song_forms.choose()

        self.duration = len(form) * 4

        self.type = 'solo'
        if number % 2:
            self.type = 'ensemble'

        if self.type == 'solo':
            if len(movement.solo_ensemble_options) == 0:
                movement.solo_ensemble_options = piece.i.get_unison_ensembles(min_notes=6)
                print 'Hey, we ran out of unison ensembles! Cool!'
            solo_ensemble_hash = random.choice(movement.solo_ensemble_options.keys())
            self.soloists = movement.solo_ensemble_options[solo_ensemble_hash]['instruments']
            self.soloist_names = [s.nickname for s in self.soloists]
            self.soloists_shared_notes = movement.solo_ensemble_options[solo_ensemble_hash]['notes']
            # Remove chosen ensemble from options
            del movement.solo_ensemble_options[solo_ensemble_hash]

            # remove chosen soloists from instrument options for the song
            for soloist in self.soloist_names:
                instrument_opts.remove(soloist)

            self.accompanist_names = instrument_opts

            len_accompanists = len(self.accompanist_names)
            if len_accompanists == 2:
                ensemble_size = 2
            elif len_accompanists == 3:
                ensemble_size = random.choice([2, 3])
            elif len_accompanists == 4:
                ensemble_size = random.choice([1, 2, 3, 4])

            self.accompanist_names = random.sample(self.accompanist_names, ensemble_size)

        else:
            # who plays, who sits out?
            ensemble_size = weighted_choice([3, 4, 5, 6], [1, 4, 5, 4])
            self.ensemble_names = random.sample(instrument_opts, ensemble_size)
            # self.ensemble = [piece.i.d[name] for name in ensemble_names]


        # make a phrase for each unique part of the form (eg, an `a` in `abacabac`)
        unique_phrases = []
        for f in set(form):
            if self.type == 'solo':
                PhraseClass = SoloPhrase
            elif self.type == 'ensemble':
                PhraseClass = EnsemblePhrase
            unique_phrases.append(PhraseClass(piece, movement, self))

        # Copy the phrases in the order specified by form
        phrases = []
        for f in form:
            phrases.append(unique_phrases[f])

        # Render phrases as music21 objects
        for phrase in phrases:
            for part in phrase.parts:
                measure = Measure()
                if movement.first_measure:
                    ts = TimeSignature('4/4')
                    measure.timeSignature = ts

                for note in part['notes']:
                    if note['pitch'] == 'rest':
                        n = Rest()
                    else:
                        p = Pitch(note['pitch'])
                        # Force all flats
                        if p.accidental.name == 'sharp':
                            p = p.getEnharmonic()
                        n = Note()

                        # TODO add slurs
                        # TODO add glissandos
                        # TODO add -50 cent marks

                    n.duration = Duration(note['duration'])

                    measure.append(n)
                piece.parts.d[part['instrument_name']].append(measure)
            movement.first_measure = False


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



    each part is a dict
    {
        'instrument_name': 'gtr'
        'notes': []
    }
    each note is a dict {
        'pitch': 44.0,
        'duration': 2.75,
        'glissando': 'start' ?
        'slur': 'start' ?
    }


    """

    def __init__(self, piece, movement, song):
        self.piece = piece
        self.movement = movement
        self.song = song
        self.parts = []

    def full_bar_rest(self):
        return {
            'pitch': 'rest',
            'duration': 4.0,
        }

    def make_resting_instruments(self, inst_names):
        for name in inst_names:
            self.parts.append({
                'instrument_name': name,
                'notes': [self.full_bar_rest()]
            })

    def make_placeholder_soloist_instruments(self, inst_names):
        for name in inst_names:
            self.parts.append({
                'instrument_name': name,
                'notes': [{
                    'pitch': 60.0,
                    'duration': 0.5
                }] * 8
            })

    def make_placeholder_accompanist_instruments(self, inst_names):
        for name in inst_names:
            self.parts.append({
                'instrument_name': name,
                'notes': [{
                    'pitch': 60.0,
                    'duration': 2.0
                }] * 2
            })



class SoloPhrase(Phrase):
    def __init__(self, piece, movement, song):
        self.piece = piece
        self.movement = movement
        self.song = song
        self.parts = []

        accompanist_names = song.accompanist_names
        soloist_names = song.soloist_names

        resting_names = []
        for name in piece.i.names:
            if name not in accompanist_names and name not in soloist_names:
                resting_names.append(name)
        self.make_resting_instruments(resting_names)

        soloists_shared_notes = song.soloists_shared_notes

        # TEMPORARY
        self.make_placeholder_soloist_instruments(soloist_names)
        self.make_placeholder_accompanist_instruments(accompanist_names)




class EnsemblePhrase(Phrase):
    def __init__(self, piece, movement, song):
        self.piece = piece
        self.movement = movement
        self.song = song
        self.parts = []

        # TEMPORARY
        self.make_resting_instruments(piece.i.names)


# class SoloMelody(object):
#     pass


# class AccompanimentMelody(object):
#     pass



class Movement1(object):
    def __init__(self, duration, piece):
        self.duration = duration
        self.songs = []
        self.solo_ensemble_options = piece.i.get_unison_ensembles(min_notes=6)
        self.first_measure = True  # just a flag so I know to make a time signature

        total = 0
        n = 0
        while total < duration:
            song = Song(n, piece, self)
            self.songs.append(song)
            total += song.duration
            n += 1
