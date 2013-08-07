import random
from dissonant_choice import get_dissonant_choices_builtin_rand_with_reorder as dissonant_choice
from weighted_choice import weighted_choice
from poetry import get_poem_structure, make_poem
from copy_Event import deepcopy_Event
from BasePiece.guitar_chords import get_fingerings_by_root_chordtype_range
from BasePiece.BaseEvent import Event, BaseEvent
from BasePiece.pitches import chordSharpsOrFlats
from BasePiece.BaseMovement import BaseMovement, Musician
from BasePiece.measure import Measure
from BasePiece.instruments import Guitar, midi_instruments, Soprano, \
     QuentinBackupVocal, PhilBackupVocal, IanBackupVocal, MattBackupVocal, \
     Clarinet, AltoSaxophone, KatieBackupVocal, BethBackupVocal, \
     JasonBackupVocal
def get_at_microbeat(mb, field):
    result = []
    for e in field:
        if mb in e.microbeats:
            result.append(e)
    return result

sustaining_keyboard_options = ['accordion', 'alto sax', 'bagpipe', 'bassoon', 
                               'brass section', 'choir aahs', 'cello', 
                               'church organ', 'clarinet', 'drawbar organ', 
                               'english horn', 'fiddle', 'flute', 'french horn', 
                               'harmonica', 'muted trumpet', 'oboe', 'ocarina', 
                               'pan flute', 'percussive organ', 'piccolo', 
                               'recorder', 'reed organ', 'rock organ', 
                               'shakuhachi', 'shanai', 'soprano sax', 
                               'string ensemble 1', 'string ensemble 2', 
                               'synth voice', 'synthbrass 1', 'synthbrass 2', 
                               'synthstrings 1', 'synthstrings 2', 'tenor sax', 
                               'trombone', 'trumpet', 'tuba', 'viola', 'violin', 
                               'voice oohs']

perc_keyboard_options = ['electric bass (finger)', 'electric guitar (jazz)', 
                         'celesta', 'electric piano 2', 'electric piano 1', 
                         'pizzicato strings', 'harpsichord', 
                         'electric guitar (muted)', 'synth bass 2', 'marimba', 
                         'koto', 'dulcimer', 'bright acoustic', 'glockenspiel', 
                         'acoustic guitar (nylon)', 'music box', 'melodic tom', 
                         'electric grand', 'acoustic bass', 'clav', 
                         'electric guitar (clean)', 'distorted guitar', 
                         'tubular bells', 'electric bass (pick)', 'sitar', 
                         'kalimba', 'synth bass 1', 'vibraphone', 'slap bass 1', 
                         'slap bass 2', 'acoustic grand', 'xylophone', 
                         'overdriven guitar', 'acoustic guitar (steel)', 
                         'banjo', 'shamisen', 'steel drums', 'fretless bass', 
                         'honky-tonk']

melody_keyboard_options = ['baritone sax', 'bagpipe', 'electric bass (finger)', 
                           'rock organ', 'electric guitar (jazz)', 'trombone', 
                           'brass section', 'celesta', 'tenor sax', 
                           'english horn', 'electric piano 2', 'clarinet', 
                           'electric piano 1', 'alto sax', 'violin', 
                           'pizzicato strings', 'accordion', 'harpsichord', 
                           'electric guitar (muted)', 'synth bass 2', 'marimba', 
                           'oboe', 'shakuhachi', 'string ensemble 1', 'koto', 
                           'reed organ', 'french horn', 'bright acoustic', 
                           'glockenspiel', 'acoustic guitar (nylon)', 
                           'church organ', 'electric grand', 'contrabass', 
                           'cello', 'acoustic bass', 'clav', 
                           'electric guitar (clean)','distorted guitar', 
                           'orchestral strings', 'concertina', 'synthstrings 2', 
                           'piccolo', 'synthstrings 1', 'electric bass (pick)', 
                           'sitar', 'synth bass 1', 'vibraphone', 'slap bass 1',
                           'trumpet', 'voice oohs', 'drawbar organ', 
                           'pan flute', 'acoustic grand', 'bassoon', 
                           'choir aahs', 'overdriven guitar', 'ocarina', 
                           'percussive organ', 'shanai', 
                           'acoustic guitar (steel)', 'viola', 
                           'string ensemble 2', 'fiddle', 'recorder', 'banjo', 
                           'flute', 'synthbrass 1', 'synthbrass 2', 
                           'synth voice', 'shamisen', 'soprano sax', 
                           'muted trumpet', 'harmonica', 'fretless bass', 
                           'honky-tonk', 'tuba']

bass_keyboard_options = ['baritone sax', 'bagpipe', 'electric bass (finger)', 
                         'rock organ', 'electric guitar (jazz)', 'trombone', 
                         'brass section', 'english horn', 'electric piano 2', 
                         'clarinet', 'electric piano 1', 'pizzicato strings', 
                         'accordion','harpsichord', 'electric guitar (muted)',
                         'synth bass 2', 'marimba', 'oboe', 'shakuhachi', 
                         'string ensemble 1', 'koto', 'reed organ', 
                         'french horn', 'bright acoustic',
                         'acoustic guitar (nylon)', 'church organ', 
                         'electric grand', 'contrabass', 'cello', 
                         'acoustic bass', 'clav', 'electric guitar (clean)', 
                         'concertina', 'synthstrings 2', 'piccolo', 
                         'synthstrings 1', 'electric bass (pick)', 'sitar', 
                         'kalimba', 'synth bass 1', 'vibraphone', 'slap bass 1', 
                         'slap bass 2', 'trumpet', 'voice oohs', 
                         'drawbar organ', 'pan flute', 'acoustic grand', 
                         'bassoon', 'choir aahs', 'ocarina', 'percussive organ', 
                         'shanai', 'acoustic guitar (steel)', 'viola', 
                         'string ensemble 2', 'fiddle', 'recorder', 'banjo',  
                         'flute', 'synthbrass 1', 'synthbrass 2', 'synth voice', 
                         'shamisen', 'soprano sax', 'muted trumpet', 
                         'blown bottle', 'harmonica', 'steel drums', 
                         'fretless bass', 'honky-tonk', 'tuba']


def init_movement():
    movement = BaseEvent(start=0)
    movement.horns = random.choice([True, False])
    movement.form = ['A', 'A', 'B', 'A', 'C', 'C', 'B', 'A']
    movement.section_type_names = list(set(movement.form))
    movement.section_types = []
    num_of_notes_in_chords = {'A':[7,6,5], 'B':[6,5,4], 'C':[5,4,3]}
    start = 0
    duration = 128
    for section_type_name in movement.section_type_names:
        section = make_section(section_type_name, movement, start, duration)
        movement.section_types.append(section)
    
    return movement

def make_section(name, movement, start, duration):
    section = BaseEvent(start=start, duration=duration)
    section.name = name
    num_ensemble_phrases = random.choice([1,2,4])
    if num_ensemble_phrases == 1:
        ensemble_phrase_form = ['A']
        ensemble_phrase_types_names= ['A']
    if num_ensemble_phrases == 2:
        ensemble_phrase_form = ['A','A']
        ensemble_phrase_types_names = ['A']
    if num_ensemble_phrases == 4:
        ensemble_phrase_form = random.choice(
            [['A','A','A','A'],['A','A','B','A'],['A','A','B','B'],
             ['A','B','A','B'],['A','A','A','B'],['A','B','B','B'],
             ['A','B','B','C'],['A','B','A','C'],['A','B','C','A'], 
             ['A','B','B','A'],['A','A','B','C'],['A','B','A','A'],
             ['A','B','C','B'],['A','B','C','C']])
        ensemble_phrase_types_names = list(set(ensemble_phrase_form))
    
    for ensemble_phrase_type_name in ensemble_phrase_types_names:
        make_ensemble_phrase(section, ensemble_phrase_type_name, num_notes_in_chords)
    
    pass

def make_ensemble_phrase(section, name):
    pass

def make_sopranos_phrase(ensemble_phrase):
    pass

def make_keyboards_phrase(ensemble_phrase):
    pass

def make_guitars_phrase(ensemble_phrase):
    pass

def make_backup_vocals_phrase(ensemble_phrase):
    pass

def init_phrase():
    phrase = BaseEvent(start=0)
    phrase.num_bars = 4
    phrase.duration = phrase.num_bars * 16
    phrase.major_scale = [0,2,4,5,7,9,11]
    phrase.chordtype_options = {
        0:[(0, 4, 7), (0, 5), (0, 5, 7), (0, 4)],# (0, 2, 5),(0, 2)],
        2:[(0, 5),(0, 3, 7),(0, 5, 7)],#(0, 2, 5),(0, 3),(0, 3, 7, 10),(0, 3, 5),(0, 2)],
        4:[(0, 5),(0, 3, 7),(0, 5, 7)],#(0, 3),(0, 3, 7, 10),(0, 3, 5)],
        5:[(0, 4, 7),(0, 4)],#(0, 2)],
        7:[(0, 4, 7), (0, 5),(0, 5, 7),(0, 4)], #(0, 2, 5), (0, 4, 7, 10),(0, 2)],
        9:[(0, 5),(0, 3, 7),(0, 5, 7)], #(0, 2, 5),(0, 3),(0, 3, 7, 10),(0, 3, 5),(0, 2)],
        11:[(0, 5)]#(0, 3),(0, 3, 5)]
    }
    phrase.key = random.choice(range(12))
    roots = [(p+phrase.key)%12 for p in phrase.major_scale]
    phrase.scale = {}
    for m, r in zip(phrase.major_scale, roots):
        phrase.scale[m] = r
    phrase.sharps_or_flats = chordSharpsOrFlats(roots)
    return phrase

def make_measures_phrase(phrase):
    phrase.measures = []

    measure_durs = [16]*phrase.num_bars
    time_sigs = [(4,4)]*phrase.num_bars
    measure_beat_durs = [[4,4,4,4]]*phrase.num_bars

    s = phrase.start
    c = 1
    for d, ts, beat_durs in zip(measure_durs, time_sigs, measure_beat_durs):
        measure = BaseEvent(duration=d, start=s)
        #bar.parents.append(movement)
        measure.time_signature = ts
        measure.beat_durs = beat_durs
        measure.beats = []
        measure.name = 'bar {0}'.format(c)
        c += 1	
        phrase.measures.append(measure)
        phrase.children.append(measure)
        s += measure.duration

    phrase.beats = []
    s = phrase.start
    c = 1
    for measure in phrase.measures:
        for d in measure.beat_durs:
            beat = BaseEvent(duration=d, start=s)
            #beat.parents.extend([bar, movement])
            beat.name = 'beat {0}'.format(c)
            c += 1
            measure.beats.append(beat)
            measure.children.append(beat)
            phrase.beats.append(beat)
            phrase.children.append(beat)
            s += beat.duration

def make_harmonies(phrase):
    harmony_phrase = BaseEvent(start=0, duration=32)
    harmony_durs = [16, 8, 8]
    num_harms = len(harmony_durs)
    harmony_roots = dissonant_choice(phrase.major_scale, num_harms)
    harmony_chordtypes = []
    for r in harmony_roots:
        chordtype = random.choice(phrase.chordtype_options[r])
        harmony_chordtypes.append(chordtype)
    harm_props = zip(harmony_durs, harmony_roots, harmony_chordtypes)

    harmony_phrase.harmonies = []
    prev_sharps_or_flats = phrase.sharps_or_flats
    s = harmony_phrase.start
    c = 1
    for d, root, chordtype in harm_props:
        harm = BaseEvent(duration=d, start=s)
        #harm.parents.append(phrase)
        harm.duration = d
        harm.root = phrase.scale[root]
        harm.chordtype = chordtype
        chord = [(p + harm.root) % 12 for p in harm.chordtype]
        harm.sharps_or_flats = chordSharpsOrFlats(chord, prev_sharps_or_flats)
        prev_sharps_or_flats = harm.sharps_or_flats
        harm.name = 'harmony {0}'.format(c)
        harmony_phrase.harmonies.append(harm)
        harmony_phrase.children.append(harm)
        #movement.children.append(harm)
        c += 1
        s += harm.duration

    harmony_phrase2 = deepcopy_Event(harmony_phrase, new_start=harmony_phrase.next_event_start)
    phrase.harmony_phrases = [harmony_phrase, harmony_phrase2]
    phrase.harmonies = []
    for hp in phrase.harmony_phrases:
        for harm in hp.harmonies:
            phrase.harmonies.append(harm)

def make_keyboard_phrase(phrase):
    keyboard_phrase = BaseEvent(start=0, duration=32)
    keyboard_durs = [16, 8, 8]
    low = random.choice(range(-10, 7))
    high = random.choice(range(19, 26))
    keyboard_phrase.register = range(low, high)
    keyboard_phrase.notes = []
    s = 0
    c = 1
    for d in keyboard_durs:
        note = Event(duration=d, start=s)
        harmony = get_at_microbeat(note.start, phrase.harmonies)
        harmony = harmony[0]
        note.sharps_or_flats = harmony.sharps_or_flats
        pitchclass_options = [(p+harmony.root)%12 for p in harmony.chordtype]
        pitch_options = [p for p in keyboard_phrase.register if p%12 in pitchclass_options]
        num_notes = random.choice(range(2,7))
        note.pitches = []
        for n in range(num_notes):
            p = random.choice(pitch_options)
            if p not in note.pitches:
                note.pitches.append(p)
            else:
                p = random.choice(pitch_options)
                if p not in note.pitches:
                    note.pitches.append(p)
        note.name = 'sustaining keyboard note {0}'.format(c)
        keyboard_phrase.notes.append(note)
        c += 1
        s += note.duration

    keyboard_phrase2 = deepcopy_Event(keyboard_phrase, new_start=keyboard_phrase.next_event_start)
    phrase.keyboard_phrases = [keyboard_phrase, keyboard_phrase2]
    phrase.keyboard_notes = []
    for kp in phrase.keyboard_phrases:
        for note in kp.notes:
            phrase.keyboard_notes.append(note)

def make_guitar_phrase(phrase):
    guitar_phrase = BaseEvent(start=0, duration=32)
    guitar_phrase_register_low = random.choice(range(-20, -9))
    guitar_phrase_register_high = random.choice(range(-5, 24))
    guitar_subphrase_durs = [16,8,8]
    guitar_note_durs = [[4,4,4,4],[4,4],[4,4]]

    guitar_phrase.subphrases = []
    s = 0
    c = 1
    for d, note_durs in zip(guitar_subphrase_durs, guitar_note_durs):
        subp = BaseEvent(duration=d, start=s)
        harmony = get_at_microbeat(subp.start, phrase.harmonies)
        harmony = harmony[0]
        subp.sharps_or_flats = harmony.sharps_or_flats
        chord_options = get_fingerings_by_root_chordtype_range(
            harmony.root, 
            harmony.chordtype,
            guitar_phrase_register_low, 
            guitar_phrase_register_high
        )
        subp.fretboard_diagram, subp.pitches = random.choice(chord_options)
        subp.note_durs = note_durs
        subp.name = 'guitar subphrase {0}'.format(c)
        guitar_phrase.subphrases.append(subp)
        c += 1
        s += subp.duration

    guitar_phrase.notes = []
    s = 0
    c = 1
    for subphrase in guitar_phrase.subphrases:
        counter = 1
        for d in subphrase.note_durs:
            note = Event(duration=d, start=s)
            note.sharps_or_flats = subphrase.sharps_or_flats
            if counter == 1:
                note.fretboard_diagram = subphrase.fretboard_diagram
            counter += 1
            note.pitches = subphrase.pitches
            note.name = 'guitar note {0}'.format(c)
            guitar_phrase.notes.append(note)
            c += 1
            s += note.duration

    guitar_phrase2 = deepcopy_Event(guitar_phrase, new_start=guitar_phrase.next_event_start)
    phrase.guitar_phrases = [guitar_phrase, guitar_phrase2]
    phrase.guitar_notes = []
    for gp in phrase.guitar_phrases:
        for note in gp.notes:
            phrase.guitar_notes.append(note)

def make_bass_phrase(phrase):
    bass_phrase = BaseEvent(start=0, duration=32)
    note_durs = [12,4,8,4,4]
    register = range(-32,5)
    scale_register = [p for p in register if p%12 in phrase.scale.values()]
    pitch_movement = [-1,-1,-1,+2,-1]
    relative_pitches = [0,-1,-2,2,1]

    bass_phrase.notes = []
    s = 0
    c = 1
    first_pitch = scale_register[len(scale_register)/2] 
    prev_pitch = first_pitch
    for d, pm in zip(note_durs, pitch_movement):
        note = Event(duration=d, start=s)
        harmony = get_at_microbeat(note.start, phrase.harmonies)
        harmony = harmony[0]
        note.sharps_or_flats = harmony.sharps_or_flats
        pitchclass_options = [(p+harmony.root)%12 for p in harmony.chordtype]	
        pitch_options = [p for p in scale_register if p%12 in pitchclass_options]
        n = random.choice(pitch_options)
        note.pitches = [n]

    #	if prev_pitch in pitch_options:
    #		i = pitch_options.index(prev_pitch)
    #		pitch_options[i+pm]
    #		note.pitches = []

        note.name = 'bass keyboard note {0}'.format(c)
        bass_phrase.notes.append(note)
        c += 1
        s += note.duration

    bass_phrase2 = deepcopy_Event(bass_phrase, new_start=bass_phrase.next_event_start)
    phrase.bass_phrases = [bass_phrase, bass_phrase2]
    phrase.bass_notes = []
    for bp in phrase.bass_phrases:
        for note in bp.notes:
            phrase.bass_notes.append(note)

def make_vocal_phrases(phrase):
    vocal_phrase_A = BaseEvent(start=0, duration=16)
    vocal_phrase_B = BaseEvent(start=vocal_phrase_A.next_event_start, duration=16)
    phrase_note_durs = [2,2,2,2,2,2,4]
    #phrase_lyric_stresses = [1,0,1,0,1,0,1]
    #poem = poetry.blahblahblah
    phrase_A_register = range(-3,12)
    phrase_B_register = range(5,20)
    phrase_A_scale_register = [p for p in phrase_A_register if p%12 in phrase.scale.values()]
    vocal_phrase_B.scale_register = [p for p in phrase_B_register if p%12 in phrase.scale.values()]

    vocal_phrase_A.notes = []
    s = vocal_phrase_A.start
    c = 1
    for d in phrase_note_durs:
        note = Event(duration=d, start=s)
        harmony = get_at_microbeat(note.start, phrase.harmonies)
        harmony = harmony[0]
        note.sharps_or_flats = harmony.sharps_or_flats
        pitchclass_options = [(p+harmony.root)%12 for p in harmony.chordtype]	
        pitch_options = [p for p in phrase_A_scale_register if p%12 in pitchclass_options]
        n = random.choice(pitch_options)
        note.pitches = [n]
        note.name = 'soprano note {0}'.format(c)
        vocal_phrase_A.notes.append(note)
        c += 1
        s += note.duration

    vocal_phrase_B.notes = []
    s = vocal_phrase_B.start
    c = 1
    for d in phrase_note_durs:
        note = Event(duration=d, start=s)
        harmony = get_at_microbeat(note.start, phrase.harmonies)
        harmony = harmony[0]
        note.sharps_or_flats = harmony.sharps_or_flats
        pitchclass_options = [(p+harmony.root)%12 for p in harmony.chordtype]	
        pitch_options = [p for p in vocal_phrase_B.scale_register if p%12 in pitchclass_options]
        n = random.choice(pitch_options)
        note.pitches = [n]
        note.name = 'soprano note {0}'.format(c)
        vocal_phrase_B.notes.append(note)
        c += 1
        s += note.duration



    vocal_phrase_C = deepcopy_Event(vocal_phrase_A, new_start=vocal_phrase_B.next_event_start)
    vocal_phrase_D = deepcopy_Event(vocal_phrase_B, new_start=vocal_phrase_C.next_event_start)

    poem_linetypes = [('A', '101010', '1'), ('B', '101010', '1')]
    poem_rawlines = [('1010101', 'A'), ('1010101', 'B'), ('1010101', 'A'), ('1010101', 'B')]
    poem_structure = get_poem_structure(poem_linetypes, poem_rawlines)
    poem = make_poem(poem_structure)


    phrase.vocal_phrases = [vocal_phrase_A, vocal_phrase_B, vocal_phrase_C, vocal_phrase_D]

    for l, p in zip(poem.lines, phrase.vocal_phrases):
        for syl, note in zip(l.syllables, p.notes):
            note.lyric = syl

    phrase.vocal_notes = []
    for vp in phrase.vocal_phrases:
        for note in vp.notes:
            phrase.vocal_notes.append(note)

    #for note, syl in zip(vocal_phrase_A.notes, poem.lines[0].syllables):		

    backup_vocal_phrase_A = BaseEvent(start=0, duration=16)
    note = Event(start=0, duration=16)
    note.pitches = []
    backup_vocal_phrase_A.notes = [note]

    backup_vocal_phrase_B = deepcopy_Event(backup_vocal_phrase_A, new_start=backup_vocal_phrase_A.next_event_start)
    backup_vocal_phrase_C = deepcopy_Event(backup_vocal_phrase_A, new_start=backup_vocal_phrase_B.next_event_start)
    backup_vocal_phrase_D = deepcopy_Event(vocal_phrase_D, new_start=backup_vocal_phrase_C.next_event_start)

    reg = range(-15,-4)
    scale_reg = [p for p in reg if p%12 in phrase.scale.values()]

    for note in backup_vocal_phrase_D.notes:
        harmony = get_at_microbeat(note.start, phrase.harmonies)
        harmony = harmony[0]
        note.sharps_or_flats = harmony.sharps_or_flats
        pitchclass_options = [(p+harmony.root)%12 for p in harmony.chordtype]	
        pitch_options = [p for p in scale_reg if p%12 in pitchclass_options]
        n = random.choice(pitch_options)
        note.pitches = [n]

    backup_vocal2_phrase_A = deepcopy_Event(backup_vocal_phrase_A)
    backup_vocal2_phrase_B = deepcopy_Event(backup_vocal_phrase_A, new_start=backup_vocal_phrase_A.next_event_start)
    backup_vocal2_phrase_C = deepcopy_Event(backup_vocal_phrase_A, new_start=backup_vocal_phrase_B.next_event_start)
    backup_vocal2_phrase_D = deepcopy_Event(vocal_phrase_D, new_start=backup_vocal_phrase_C.next_event_start)

    for note in backup_vocal2_phrase_D.notes:
        harmony = get_at_microbeat(note.start, phrase.harmonies)
        harmony = harmony[0]
        note.sharps_or_flats = harmony.sharps_or_flats
        pitchclass_options = [(p+harmony.root)%12 for p in harmony.chordtype]	
        pitch_options = [p for p in scale_reg if p%12 in pitchclass_options]
        n = random.choice(pitch_options)
        note.pitches = [n]


    phrase.backup_vocal1_phrases = [backup_vocal_phrase_A, backup_vocal_phrase_B, backup_vocal_phrase_C, backup_vocal_phrase_D]
    phrase.backup_vocal1_notes = []
    for vp in phrase.backup_vocal1_phrases:
        for note in vp.notes:
            phrase.backup_vocal1_notes.append(note)

    phrase.backup_vocal2_phrases = [backup_vocal2_phrase_A, backup_vocal2_phrase_B, backup_vocal2_phrase_C, backup_vocal2_phrase_D]
    phrase.backup_vocal2_notes = []
    for vp in phrase.backup_vocal2_phrases:
        for note in vp.notes:
            phrase.backup_vocal2_notes.append(note)


def make_movement(movement):
    
    phrase = init_phrase()
    make_measures_phrase(phrase)
    make_harmonies(phrase)
    make_keyboard_phrase(phrase)
    make_guitar_phrase(phrase)
    make_bass_phrase(phrase)
    make_vocal_phrases(phrase)

    phrase2 = deepcopy_Event(phrase, new_start=phrase.next_event_start)
    movement.phrases = [phrase, phrase2]
    movement.measures = []
    movement.harmonies = []
    movement.keyboard_notes = []
    movement.guitar_notes = []
    movement.bass_notes = []
    movement.vocal_notes = []
    movement.backup_vocal1_notes = []
    movement.backup_vocal2_notes = []

    for p in movement.phrases:
        for m in p.measures:
            movement.measures.append(m)
        for h in p.harmonies:
            movement.harmonies.append(h)
        for n in p.keyboard_notes:
            movement.keyboard_notes.append(n)
        for n in p.guitar_notes:
            movement.guitar_notes.append(n)
        for n in p.bass_notes:
            movement.bass_notes.append(n)
        for n in p.vocal_notes:
            movement.vocal_notes.append(n)
        for n in p.backup_vocal1_notes:
            movement.backup_vocal1_notes.append(n)
        for n in p.backup_vocal2_notes:
            movement.backup_vocal2_notes.append(n)
    return movement


class MvmtType10(BaseMovement):
    def __init__(self, piece, movement_name, seq_number, folder_name, file_name_prefix, main_title, subtitle):
        self.folder_name = folder_name
        self.file_name_prefix = file_name_prefix
        self.main_title = main_title
        self.subtitle = subtitle
        BaseMovement.__init__(self, piece, movement_name, seq_number)        

        self.tempo_duration = 4
        self.tempo_bpm = 60
        self.duration_denominator = 16
        
        
        movement = init_movement()        
        
        self.choose_ensemble(movement)
        
        movement.musicians = self.musicians
        
        make_movement(movement)      

        #for phrase in movement.phrases:
        self.musicians_by_name['Erin'].music.extend(movement.vocal_notes)
        self.musicians_by_name['Laura'].music.extend(movement.vocal_notes)
        self.musicians_by_name['QuentinVoice'].music.extend(movement.backup_vocal1_notes)
        self.musicians_by_name['Quentin'].music.extend(movement.keyboard_notes)
        self.musicians_by_name['PhilVoice'].music.extend(movement.backup_vocal1_notes)
        self.musicians_by_name['Phil'].music.extend(movement.keyboard_notes)
        self.musicians_by_name['Will'].music.extend(movement.bass_notes)
        self.musicians_by_name['MattVoice'].music.extend(movement.backup_vocal2_notes)
        self.musicians_by_name['Matt'].music.extend(movement.guitar_notes)    
        self.musicians_by_name['IanVoice'].music.extend(movement.backup_vocal2_notes)
        self.musicians_by_name['Ian'].music.extend(movement.guitar_notes) 
        self.musicians_by_name['Katie'].music.extend(movement.backup_vocal1_notes)
        self.musicians_by_name['Beth'].music.extend(movement.backup_vocal2_notes)
        self.musicians_by_name['Jason'].music.extend(movement.backup_vocal2_notes)

        self.make_meter(movement)
        BaseMovement.ly_closeout(self)

    def choose_ensemble(self, movement):
        self.musicians = []

        erin = Musician(Soprano())
        erin.name = 'Erin'
        erin.instrument.name = 'Erin Soprano'
        erin.instrument.short_name = 'ES'
        erin.lyrics = True
        self.musicians.append(erin)

        laura = Musician(Soprano())
        laura.name = 'Laura'
        laura.instrument.name = 'Laura Soprano'
        laura.instrument.short_name = 'LS'
        laura.lyrics = True
        self.musicians.append(laura)

        quentin_voice = Musician(QuentinBackupVocal())
        quentin_voice.name = 'QuentinVoice'
        quentin_voice.part_group = 'Quentin'
        quentin_voice.lyrics = True
        self.musicians.append(quentin_voice)

        keyboard_instrument = random.choice(sustaining_keyboard_options)
        quentin = Musician(midi_instruments[keyboard_instrument])
        quentin.name = 'Quentin'
        quentin.part_group = 'Quentin'
        self.musicians.append(quentin)
        self.part_groups['Quentin'] = [quentin_voice, quentin]        

        phil_voice = Musician(PhilBackupVocal())
        phil_voice.name = 'PhilVoice'
        phil_voice.part_group = 'Phil'
        phil_voice.lyrics = True
        self.musicians.append(phil_voice)

        keyboard_instrument = random.choice(sustaining_keyboard_options)
        phil = Musician(midi_instruments[keyboard_instrument])
        phil.name = 'Phil'
        phil.part_group = 'Phil'
        self.musicians.append(phil)
        self.part_groups['Phil'] = [phil_voice, phil]   

        bass_keyboard_instrument = random.choice(bass_keyboard_options)
        will = Musician(midi_instruments[bass_keyboard_instrument])
        will.name = 'Will'
        self.musicians.append(will)

        matt_voice = Musician(MattBackupVocal())
        matt_voice.name = 'MattVoice'
        matt_voice.lyrics = True
        matt_voice.part_group = 'Matt'
        self.musicians.append(matt_voice) 

        matt = Musician(Guitar())
        matt.name = 'Matt'
        matt.instrument.name = 'Matt Guitar'
        matt.instrument.short_name = 'MG'
        matt.part_group = 'Matt'
        self.musicians.append(matt)
        self.part_groups['Matt'] = [matt_voice, matt]

        ian_voice = Musician(IanBackupVocal())
        ian_voice.name = 'IanVoice'
        ian_voice.lyrics = True
        ian_voice.part_group = 'Ian'
        self.musicians.append(ian_voice) 

        ian = Musician(Guitar())
        ian.name = 'Ian'
        ian.instrument.name = 'Ian Guitar'
        ian.instrument.short_name = 'IG'
        ian.part_group = 'Ian'
        self.musicians.append(ian)
        self.part_groups['Ian'] = [ian_voice, ian]

        if movement.horns == True:        
            katie = Musician(Clarinet())
            katie.name = 'Katie'
            katie.lyrics = True
            self.musicians.append(katie)

            beth = Musician(AltoSaxophone())
            beth.name = 'Beth'
            beth.instrument.name = 'Beth Alto Sax'
            beth.instrument.short_name = 'BS'
            beth.lyrics = True
            self.musicians.append(beth)

            jason = Musician(AltoSaxophone())
            jason.name = 'Jason'
            jason.instrument.name = 'Jason Alto Sax'
            jason.instrument.short_name = 'JS'
            jason.lyrics = True
            self.musicians.append(jason) 
        else:
            katie = Musician(KatieBackupVocal())
            katie.name = 'Katie'
            katie.lyrics = True
            self.musicians.append(katie) 

            beth = Musician(BethBackupVocal())
            beth.name = 'Beth'
            beth.lyrics = True
            self.musicians.append(beth)      

            jason = Musician(JasonBackupVocal())
            jason.name = 'Jason'
            jason.lyrics = True
            self.musicians.append(jason) 

        self.musicians_by_name = {}
        for m in self.musicians:
            self.musicians_by_name[m.name] = m

    def make_meter(self, movement):
        start = 0
        for measure in movement.measures:
            m = Measure(measure.time_signature[0], measure.time_signature[1], self.duration_denominator, start)
            self.measures.append(m)
            start = m.next_measure_start

