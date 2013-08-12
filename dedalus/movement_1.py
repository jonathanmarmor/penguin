import random
from collections import defaultdict

from music21.note import Note, Rest
from music21.pitch import Pitch
from music21.stream import Stream, Measure
from music21.meter import TimeSignature
from music21.duration import Duration
from music21.spanner import Glissando, Slur

from utils import weighted_choice, count_intervals, frange
import song_forms


def get_harmonies(parts):
    beat_map = defaultdict(list)
    for part in parts:
        beat = 0
        for note in part['notes']:
            dur = int(note['duration'] * 4)
            for b in range(dur):
                if note['pitch'] != 'rest':
                    beat_map[beat].append(note)
                beat += 1

    harmonies = []
    for beat in beat_map:
        harmony = []
        for note in beat_map[beat]:
            harmony.append(note['pitch'])
        harmonies.append(harmony)
    return harmonies


def validate_harmony(harmony):
    harmony = list(set([int(p % 12) for p in harmony]))
    harmony.sort()
    lowest = min(harmony)
    harmony = [p - lowest for p in harmony]

    interval_count = count_intervals(harmony)
    intervals = interval_count.keys()
    if set([1, 6, 11]).intersection(intervals):
        return False

    if harmony == [0, 4, 8]:
        return False

    return True


# def choose_pitches(parts):
#     for part in parts:
#         for note in part['notes']:
#             if note['pitch'] != 'rest':
#                 note['pitch'] = random.choice(part['note_opts'])

#     harmonies = get_harmonies(parts)
#     valid = all([validate_harmony(h) for h in harmonies])
#     if not valid:
#         choose_pitches(parts)


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


class SoloPhrase(Phrase):
    def __init__(self, piece, movement, song):
        self.piece = piece
        self.movement = movement
        self.song = song
        self.parts = []

        accompanist_names = self.accompanist_names = song.accompanist_names
        soloist_names = self.soloist_names = song.soloist_names

        resting_names = []
        for name in piece.i.names:
            if name not in accompanist_names and name not in soloist_names:
                resting_names.append(name)
        self.make_resting_instruments(resting_names)

        soloists_shared_notes = song.soloists_shared_notes

        self.make_accompanists(accompanist_names)

        self.make_soloists(soloist_names)

        self.choose_pitches(self.parts)

    def make_accompanists(self, accompanist_names):
        # Make a new rhythm for each accompanist
        for name in accompanist_names:
            self.parts.append({
                'instrument_name': name,
                'notes': AccompanimentMelody().notes
            })

    def make_soloists(self, soloist_names):
        # Make one rhythm and assign it to all soloists
        notes = SoloMelody().notes
        for name in soloist_names:
            self.parts.append({
                'instrument_name': name,
                'notes': notes
            })

    def choose_pitches(self, parts):
        # Temporary
        for part in parts:
            for note in part['notes']:
                if note['pitch'] != 'rest':
                    note['pitch'] = 'rest'  # random.choice(part['note_opts'])

        # harmonies = get_harmonies(parts)
        # valid = all([validate_harmony(h) for h in harmonies])
        # if not valid:
        #     self.choose_pitches(parts)


class EnsemblePhrase(Phrase):
    def __init__(self, piece, movement, song):
        self.piece = piece
        self.movement = movement
        self.song = song
        self.parts = []

        ensemble_names = song.ensemble_names

        resting_names = []
        for name in piece.i.names:
            if name not in ensemble_names:
                resting_names.append(name)
        self.make_resting_instruments(resting_names)

        self.make_soloists(ensemble_names)

        self.choose_pitches(self.parts)

    def make_soloists(self, soloist_names):
        # Make a new rhythm for each soloist
        for name in soloist_names:
            self.parts.append({
                'instrument_name': name,
                'notes': SoloMelody().notes,
                'all_note_opts': self.piece.i.d[name].all_notes,
                'note_opts': self.piece.i.d[name].all_notes
            })

    def choose_pitches(self, parts):
        for part in parts:
            for note in part['notes']:
                if note['pitch'] != 'rest':
                    note['pitch'] = random.choice(part['note_opts'])
                    # reset note_opts to a range within a 4th in either direction of the chosen note,
                    # but making sure that all notes are in all_note_opts
                    part['note_opts'] = [p for p in frange(note['pitch'] - 5, note['pitch'] + 6) if p in part['all_note_opts']]
        print parts


        harmonies = get_harmonies(parts)
        valid = all([validate_harmony(h) for h in harmonies])
        if not valid:
            self.choose_pitches(parts)



class SoloMelody(object):
    def __init__(self):
        self.notes = [{
            'pitch': None,
            'duration': 0.5
        }] * 8


class AccompanimentMelody(object):
    def __init__(self):
        self.notes = [{
            'pitch': None,
            'duration': 2.0
        }] * 2


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
