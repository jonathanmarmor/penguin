from BasePiece.BaseEvent import Event, BaseEvent
from copy_Event import deepcopy_Event
from BasePiece.pitches import chordSharpsOrFlats
import random
import itertools
from BasePiece.common_combinations import thirtytwo, sixtyfour
from BasePiece.chordtypes import get_chordtype
from Movements.MvmtType10_chordtypes import preferred_chordtypes, \
     all_chordtypes, dissonant_chordtypes
from build_chord_options import chordtypes_on_roots

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

def make_movement(mv_type10):
    movement = BaseEvent(start=0)
    movement.musicians = ['Erin', 'Laura', 'QuentinVoice', 'Quentin', 
                          'PhilVoice', 'Phil', 'Will', 'MattVoice', 'Matt', 
                          'IanVoice', 'Katie', 'Beth', 'Jason']
    movement.tempo_bpm = random.choice(range(66,85,2))
    movement.schizoid_harmony = random.choice([True, False, False, False, False])
    movement.harmonies_tracker = []
    movement.horns = mv_type10.horns
    movement.musicians = mv_type10.musicians
    
    seg_order_opts = {
        8: [
            ['I', 'I', 'II', 'I', 'III', 'III', 'II', 'I'],
            ['I', 'I', 'I', 'II', 'III', 'III', 'II', 'I'],
            ['I', 'II', 'I', 'II', 'III', 'III', 'II', 'I'],
            ['I', 'II', 'I', 'II', 'III', 'III', 'III', 'I'],
            ['I', 'II', 'I', 'III', 'III', 'III', 'II', 'I']        
            ],
        9: [
            ['I', 'I', 'I', 'II', 'III', 'III', 'III', 'II', 'I'],
            ['I', 'I', 'II', 'I', 'III', 'III', 'II', 'I', 'I'],
            ['I', 'I', 'II', 'III', 'III', 'III', 'II', 'I', 'I']        
            ],
        10: [
            ['I', 'I', 'I', 'II', 'I', 'III', 'III', 'III', 'II', 'I'],
            ['I', 'I', 'II', 'II', 'I', 'II', 'III', 'III', 'II', 'I'],
            ['I', 'II', 'I', 'II', 'III', 'III', 'II', 'III', 'II', 'I'],
            ['I', 'I', 'II', 'I', 'II', 'II', 'III', 'III', 'II', 'I']          
            ],
        11: [
            ['I', 'I', 'II', 'I', 'I', 'II', 'III', 'III', 'II', 'I', 'I'],
            ['I', 'II', 'I', 'II', 'I', 'III', 'III', 'III', 'I', 'II', 'I'],    
            ['I', 'I', 'I', 'II', 'II', 'II', 'III', 'III', 'III', 'II', 'I'],
            ['I', 'II', 'III', 'I', 'II', 'III', 'III', 'I', 'II', 'III', 'I'],
            ['I', 'I', 'II', 'II', 'I', 'I', 'III', 'III', 'II', 'I', 'I']
        ]
    }

    if movement.tempo_bpm == 66: num_segs = [8,9]
    if movement.tempo_bpm == 68: num_segs = [8,9]        
    if movement.tempo_bpm == 70: num_segs = [8,9]
    if movement.tempo_bpm == 72: num_segs = [8,9,10]
    if movement.tempo_bpm == 74: num_segs = [8,9,10]
    if movement.tempo_bpm == 76: num_segs = [8,9,10]
    if movement.tempo_bpm == 78: num_segs = [8,9,10]
    if movement.tempo_bpm == 80: num_segs = [9,10,11]        
    if movement.tempo_bpm == 82: num_segs = [10,11]
    if movement.tempo_bpm == 84: num_segs = [10,11]

    movement.segment_order_options = []
    for num in num_segs:
        movement.segment_order_options.extend(seg_order_opts[num])



    movement.segment_order = random.choice(movement.segment_order_options)

    movement.duration_of_segments = 128
    calculate_duration(movement)

    movement.segment_type_names = list(set(movement.segment_order))
    movement.subsegment_order_options = {
        1: [['A']],
        2: [['A','A']],
        4: [['A','A','A','A'],['A','A','B','A'],['A','A','B','B'],
            ['A','B','A','B'],['A','A','A','B'],['A','B','B','B'],
            ['A','B','B','C'],['A','B','A','C'],['A','B','C','A'], 
            ['A','B','B','A'],['A','A','B','C'],['A','B','A','A'],
            ['A','B','C','B'],['A','B','C','C']]
    }    
    movement.segment_types = {}
    for type_name in movement.segment_type_names:
        make_section_types(type_name, movement)   
    return movement

def calculate_duration(movement):
    dur_of_sixteenths = 60.0/(movement.tempo_bpm*4)
    len_of_segments = movement.duration_of_segments
    num_of_segments = len(movement.segment_order)
    movement.duration = len_of_segments * num_of_segments
    movement.duration_seconds = dur_of_sixteenths * movement.duration

def make_section_types(name, movement):
    section_type = BaseEvent(start=0, duration=movement.duration_of_segments)
    section_type.name = name
    section_type.movement = movement
    section_type.num_of_segments = random.choice([1,2,4])
    section_type.segment_order = random.choice(movement.subsegment_order_options[section_type.num_of_segments])
    section_type.segment_type_names = list(set(section_type.segment_order))    
    movement.segment_types[name] = section_type 
    section_type.segment_types = {}
    section_type.schizoid_harmony = movement.schizoid_harmony
    make_harmony_options(section_type)

    for type_name in section_type.segment_type_names:
        make_phrase_types(type_name, section_type)

def make_phrase_types(name, section_type):        
    d = section_type.duration/section_type.num_of_segments
    phrase_type = BaseEvent(start=0, duration=d)    
    section_type.segment_types[name] = phrase_type    
    phrase_type.name = name
    phrase_type.section_type = section_type
    phrase_type.movement = section_type.movement
    phrase_type.harmony_options = section_type.harmony_options

    make_measures(phrase_type)
    make_harmonic_rhythm(phrase_type)
    make_harmonies(phrase_type)
    
    phrase_type.notes = {}
    for musician in phrase_type.movement.musicians:
        phrase_type.notes[musician.name] = []
    
    TEMP_make_keyboard_register(phrase_type, 'Will')    
    TEMP_make_keyboard_rhythms(phrase_type, 'Will')
    TEMP_make_keyboard_notes(phrase_type, 'Will')

#---------------------------------------    
def make_measures(segment):
    segment.measures = []
    s = segment.start
    for x in range(segment.duration/16):
        m = BaseEvent(start=s, duration=16)
        m.time_signature = (4,4)
        s = m.next_event_start

#---------------------------------------
def make_harmonic_rhythm(segment):
    if segment.duration == 128:
        rhythm_options = sixtyfour
        segment.harmonic_rhythm = random.choice(rhythm_options) + random.choice(rhythm_options)
    if segment.duration == 64:
        rhythm_options = sixtyfour
        segment.harmonic_rhythm = random.choice(rhythm_options)
    if segment.duration == 32:
        rhythm_options = thirtytwo
        segment.harmonic_rhythm = random.choice(rhythm_options)

#---------------------------------------
def make_harmony_options(segment):
    segment.chordtypes = []
    if segment.schizoid_harmony:
        print 'schizoid harmony!'
        chordtypes = preferred_chordtypes[3] + preferred_chordtypes[3] + \
                   preferred_chordtypes[3] + preferred_chordtypes[3] + \
                   preferred_chordtypes[3] + dissonant_chordtypes[5] + \
                   dissonant_chordtypes[6]
    else:
        if segment.name == 'I':
            chordtypes = preferred_chordtypes[7] + preferred_chordtypes[7] +\
                       preferred_chordtypes[6] + preferred_chordtypes[5]
        if segment.name == 'II':
            chordtypes = preferred_chordtypes[6] + \
                       preferred_chordtypes[5] + preferred_chordtypes[4]    
        if segment.name == 'III':
            chordtypes = preferred_chordtypes[5] + preferred_chordtypes[4] + \
                       preferred_chordtypes[3] + preferred_chordtypes[3]
    segment.harmony_options = chordtypes_on_roots(chordtypes)
#---------------------------------------
def make_harmonies(segment):
    segment.harmonies = []
    previous_chord = random.choice(segment.harmony_options)
    prev_sharps_or_flats = 'sharps'
    s = segment.start
    for d in segment.harmonic_rhythm:
        harmony = BaseEvent(start=s, duration=d)
        s += d
        harmony.pitches = get_chord(segment, previous_chord)
        harmony.sharps_or_flats = chordSharpsOrFlats(harmony.pitches, prev_sharps_or_flats)        
        segment.harmonies.append(harmony)
        segment.movement.harmonies_tracker.append(harmony)
        previous_chord = harmony.pitches     

def get_chord(segment, previous):
    prev = [previous]*len(segment.harmony_options)
    opts = map(include_harmony, segment.harmony_options, prev)
    opts = [o for o in opts if o]
    chord = random.choice(opts)
    return chord

def include_harmony(chord, prev):
##    if get_chordtype(chord) is not (0,4,7):
##        if chord in segment.movement.harmonies_tracker:
##            return False
    if common(prev, chord) < 1:
        return False
    if added(prev, chord) < 1:
        return False 
    if len(chord) > 3 or len(prev) > 3:
        if common(prev, chord) < 2:
            return False   
    if len(chord) > 4 and len(prev) > 4:
        if common(prev, chord) < 3:
            return False
    if len(chord) > 5 and len(prev) > 5:
        if common(prev, chord) < 4:
            return False

    else:
        return chord

def common(list1, list2):
    '''return the number of items that are in both list #1 and list #2'''
    return len(set(list1) & set(list2))

def drop_out(list1, list2):
    '''return the number of items that are in list #1 but not in list #2'''
    return len( set( list1 ) - set( list2 ) )

def added(list1, list2):
    '''return the number of items that are in list #2 but not in list #1'''
    return len( set( list2 ) - set( list1 ) )

#---------------------------------------
def TEMP_make_keyboard_register(segment, musician_name):
    segment.register[musician_name] = segment.movement.musicians[musician_name].instrument.register
    
def TEMP_make_keyboard_rhythms(segment, musician_name):
    segment.rhythm[musician_name] = segment.harmonic_rhythm
    
def TEMP_make_keyboard_notes(segment, musician_name):
    for d in segment.rhythm[musician_name]:
        note = Event(duration=d, start=segment.start)
        
        harmony = get_at_microbeat(note.start, phrase.harmonies)
        harmony = harmony[0]
        note.sharps_or_flats = harmony.sharps_or_flats
        
        pitch_options = [p for p in segment.register[musician_name] if p%12 in harmony.pitches]
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
        segment.notes[musician.name].append(note)
    
    
    
#---------------------------------------
def make_phrases(movement):   
    for section_type_name in movement.segment_types:
        section = movement.segment_types[section_type_name]
        section.segments = []
        s = section.start
        for phrase_type_name in section.segment_order:
            phrase = section.segment_types[phrase_type_name]
            new_phrase = deepcopy_Event(phrase, new_start=s)
            section.segments.append(new_phrase)
            s += new_phrase.duration

def make_sections(movement):
    movement.segments = []
    s = movement.start
    for section_type_name in movement.segment_order:
        section = movement.segment_types[section_type_name]
        new_section = deepcopy_Event(section, new_start=s)
        movement.segments.append(new_section)
        s += new_section.duration

def put_notes_in_movement(movement):
    for section in movement.segments:
        for phrase in section.phrases:
            movement.measures.extend(phrase.measures)
            movement.harmonies.extend(phrase.harmonies)
            for musician in movement.musicians:
                movement.notes[musician.name].extend(phrase.notes[musician.name])            


#---------------------------------------
def main(mv_type10):
    movement = make_movement(mv_type10)


    make_phrases(movement)
    make_sections(movement)
    #put_notes_in_movement(movement)

    print movement.tempo_bpm
    print len(movement.segment_order)
    print movement.duration
    print movement.duration_seconds
    for section in movement.segments:
        print section.name
        for phrase in section.segments:
            print '\t', phrase.name, phrase.duration
            for r, h in zip(phrase.harmonic_rhythm, phrase.harmonies):
                print '\t\t{0:<5}{1}'.format(r, h)

    return movement

class MvmtType10(BaseMovement):
    def __init__(self, piece, movement_name, seq_number, folder_name, file_name_prefix, main_title, subtitle):
        self.folder_name = folder_name
        self.file_name_prefix = file_name_prefix
        self.main_title = main_title
        self.subtitle = subtitle
        BaseMovement.__init__(self, piece, movement_name, seq_number)        

        self.horns = random.choice([True, False])
        self.choose_ensemble()        
        
        
        movement = main()        

        
        self.tempo_duration = 4
        self.tempo_bpm = movement.tempo_bpm
        self.duration_denominator = 16        
     

        #for phrase in movement.phrases:
##        self.musicians_by_name['Erin'].music.extend(movement.vocal_notes)
##        self.musicians_by_name['Laura'].music.extend(movement.vocal_notes)
##        self.musicians_by_name['QuentinVoice'].music.extend(movement.backup_vocal1_notes)
##        self.musicians_by_name['Quentin'].music.extend(movement.keyboard_notes)
##        self.musicians_by_name['PhilVoice'].music.extend(movement.backup_vocal1_notes)
##        self.musicians_by_name['Phil'].music.extend(movement.keyboard_notes)
        self.musicians_by_name['Will'].music.extend(movement.bass_notes)
##        self.musicians_by_name['MattVoice'].music.extend(movement.backup_vocal2_notes)
##        self.musicians_by_name['Matt'].music.extend(movement.guitar_notes)    
##        self.musicians_by_name['IanVoice'].music.extend(movement.backup_vocal2_notes)
##        self.musicians_by_name['Ian'].music.extend(movement.guitar_notes) 
##        self.musicians_by_name['Katie'].music.extend(movement.backup_vocal1_notes)
##        self.musicians_by_name['Beth'].music.extend(movement.backup_vocal2_notes)
##        self.musicians_by_name['Jason'].music.extend(movement.backup_vocal2_notes)

        self.make_meter(movement)
        BaseMovement.ly_closeout(self)

    def choose_ensemble(self, movement):
        self.musicians = []

##        erin = Musician(Soprano())
##        erin.name = 'Erin'
##        erin.instrument.name = 'Erin Soprano'
##        erin.instrument.short_name = 'ES'
##        erin.lyrics = True
##        self.musicians.append(erin)
##
##        laura = Musician(Soprano())
##        laura.name = 'Laura'
##        laura.instrument.name = 'Laura Soprano'
##        laura.instrument.short_name = 'LS'
##        laura.lyrics = True
##        self.musicians.append(laura)
##
##        quentin_voice = Musician(QuentinBackupVocal())
##        quentin_voice.name = 'QuentinVoice'
##        quentin_voice.part_group = 'Quentin'
##        quentin_voice.lyrics = True
##        self.musicians.append(quentin_voice)
##
##        keyboard_instrument = random.choice(sustaining_keyboard_options)
##        quentin = Musician(midi_instruments[keyboard_instrument])
##        quentin.name = 'Quentin'
##        quentin.part_group = 'Quentin'
##        self.musicians.append(quentin)
##        self.part_groups['Quentin'] = [quentin_voice, quentin]        
##
##        phil_voice = Musician(PhilBackupVocal())
##        phil_voice.name = 'PhilVoice'
##        phil_voice.part_group = 'Phil'
##        phil_voice.lyrics = True
##        self.musicians.append(phil_voice)
##
##        keyboard_instrument = random.choice(sustaining_keyboard_options)
##        phil = Musician(midi_instruments[keyboard_instrument])
##        phil.name = 'Phil'
##        phil.part_group = 'Phil'
##        self.musicians.append(phil)
##        self.part_groups['Phil'] = [phil_voice, phil]   

        bass_keyboard_instrument = random.choice(bass_keyboard_options)
        will = Musician(midi_instruments[bass_keyboard_instrument])
        will.name = 'Will'
        self.musicians.append(will)

##        matt_voice = Musician(MattBackupVocal())
##        matt_voice.name = 'MattVoice'
##        matt_voice.lyrics = True
##        matt_voice.part_group = 'Matt'
##        self.musicians.append(matt_voice) 
##
##        matt = Musician(Guitar())
##        matt.name = 'Matt'
##        matt.instrument.name = 'Matt Guitar'
##        matt.instrument.short_name = 'MG'
##        matt.part_group = 'Matt'
##        self.musicians.append(matt)
##        self.part_groups['Matt'] = [matt_voice, matt]
##
##        ian_voice = Musician(IanBackupVocal())
##        ian_voice.name = 'IanVoice'
##        ian_voice.lyrics = True
##        ian_voice.part_group = 'Ian'
##        self.musicians.append(ian_voice) 
##
##        ian = Musician(Guitar())
##        ian.name = 'Ian'
##        ian.instrument.name = 'Ian Guitar'
##        ian.instrument.short_name = 'IG'
##        ian.part_group = 'Ian'
##        self.musicians.append(ian)
##        self.part_groups['Ian'] = [ian_voice, ian]
##
##        if movement.horns == True:        
##            katie = Musician(Clarinet())
##            katie.name = 'Katie'
##            katie.lyrics = True
##            self.musicians.append(katie)
##
##            beth = Musician(AltoSaxophone())
##            beth.name = 'Beth'
##            beth.instrument.name = 'Beth Alto Sax'
##            beth.instrument.short_name = 'BS'
##            beth.lyrics = True
##            self.musicians.append(beth)
##
##            jason = Musician(AltoSaxophone())
##            jason.name = 'Jason'
##            jason.instrument.name = 'Jason Alto Sax'
##            jason.instrument.short_name = 'JS'
##            jason.lyrics = True
##            self.musicians.append(jason) 
##        else:
##            katie = Musician(KatieBackupVocal())
##            katie.name = 'Katie'
##            katie.lyrics = True
##            self.musicians.append(katie) 
##
##            beth = Musician(BethBackupVocal())
##            beth.name = 'Beth'
##            beth.lyrics = True
##            self.musicians.append(beth)      
##
##            jason = Musician(JasonBackupVocal())
##            jason.name = 'Jason'
##            jason.lyrics = True
##            self.musicians.append(jason) 

        self.musicians_by_name = {}
        for m in self.musicians:
            self.musicians_by_name[m.name] = m

    def make_meter(self, movement):
        start = 0
        for measure in movement.measures:
            m = Measure(measure.time_signature[0], measure.time_signature[1], self.duration_denominator, start)
            self.measures.append(m)
            start = m.next_measure_start


##if __name__ == '__main__':
##    main()











