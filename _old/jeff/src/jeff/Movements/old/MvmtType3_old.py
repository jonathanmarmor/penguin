# Movement type 3
# I 3
# Movements 9, 10

from BasePiece.BaseEvent import Event, BaseEvent
from copy_Event import deepcopy_Event
from BasePiece.pitches import chordSharpsOrFlats
from BasePiece.guitar_chords import get_fingerings_by_root_chordtype_range
import random
from weighted_choice import weighted_choice
import itertools
from BasePiece.common_combinations import thirtytwo, sixtyfour
from BasePiece.chordtypes import get_chordtype
from Movements.MvmtType5_chordtypes import preferred_chordtypes

from Movements.MvmtType10_instruments import sustaining_keyboard_options, \
    perc_keyboard_options, melody_keyboard_options, bass_keyboard_options
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

def make_movement(mv_type):
    movement = BaseEvent(start=0)
    movement.musicians = ['Erin', 'Laura', 'QuentinVoice', 'Quentin', 
                          'PhilVoice', 'Phil', 'Will', 'MattVoice', 'Matt', 
                          'IanVoice', 'Katie', 'Beth', 'Jason']
    movement.measures = []
    movement.harmonies = []
    movement.notes = {}
    movement.tempo_bpm = random.choice(range(54,105,2))
    movement.schizoid_harmony = random.choice([True, False, False, False, False])
    movement.harmonies_tracker = []
    movement.horns = mv_type.horns
    movement.sections_with_horns = random.choice([['III'], ['III'], ['II','III'], ['I','II'], ['II']])
    movement.musicians = mv_type.musicians
    movement.musicians_by_name = mv_type.musicians_by_name
    
    seg_order_opts = {
        6: [
            ['I', 'I' 'II', 'III', 'II', 'I'],
            ['I', 'I' 'II', 'III', 'I', 'II'],            
            ['I', 'II' 'I', 'III', 'I', 'II'],
            ['I', 'II' 'I', 'III', 'II', 'I'],
            ['I', 'II' 'I', 'III', 'III', 'II'],            
            ['I', 'II' 'I', 'III', 'III', 'I'],
            ['I', 'I' 'II', 'I' 'III', 'I'],
            ['I', 'II' 'I', 'III' 'I', 'II'],
            ['I', 'I' 'I', 'II', 'III', 'II']            
            ],
        7: [
            ['I', 'I' 'II', 'I' 'III', 'III', 'II'],             
            ['I', 'I' 'II', 'I' 'III', 'III', 'I'],            
            ['I', 'II' 'I', 'II' 'III', 'III', 'II'],            
            ['I', 'II' 'I', 'II' 'III', 'III', 'I'],             
            ['I', 'II' 'I', 'III' 'III', 'III', 'II'],  
            ['I', 'II' 'I', 'III' 'III', 'III', 'I'],            
            ['I', 'II' 'I', 'III' 'I', 'III', 'I'],            
            ['I', 'II' 'I', 'III' 'I', 'II', 'I'],
            ['I', 'II' 'II', 'II', 'I', 'III', 'I'],            
            ['I', 'I' 'I', 'II', 'I', 'III', 'I']            
            ],      
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
            ['I', 'I', 'II', 'II', 'I', 'I', 'III', 'III', 'II', 'I', 'I'],
            ],
        12: [
            ['I', 'I', 'II', 'I', 'II', 'II', 'III', 'II', 'I', 'I', 'II', 'I', ],
            ['I', 'I', 'II', 'I', 'I', 'II', 'III', 'III', 'II', 'I', 'I', 'II', ],
            ['I', 'II', 'II', 'I', 'II', 'II', 'III', 'II', 'II', 'I', 'II', 'II'],        
            ['I', 'II', 'I', 'III', 'I', 'II', 'I', 'III', 'III', 'II', 'I', 'II'],         
            ['I', 'II', 'I', 'II', 'I', 'II', 'III', 'III', 'III', 'I', 'II', 'I']       
        ]
    }

    if movement.tempo_bpm == 54: num_segs = [6]
    if movement.tempo_bpm == 56: num_segs = [6]
    if movement.tempo_bpm == 58: num_segs = [6]
    if movement.tempo_bpm == 60: num_segs = [6, 7]
    if movement.tempo_bpm == 62: num_segs = [7]
    if movement.tempo_bpm == 64: num_segs = [7]
    if movement.tempo_bpm == 66: num_segs = [7]
    if movement.tempo_bpm == 68: num_segs = [7, 8]
    if movement.tempo_bpm == 70: num_segs = [7, 8]
    if movement.tempo_bpm == 72: num_segs = [8]
    if movement.tempo_bpm == 74: num_segs = [8]
    if movement.tempo_bpm == 76: num_segs = [8, 9]
    if movement.tempo_bpm == 78: num_segs = [8, 9]
    if movement.tempo_bpm == 80: num_segs = [8, 9]
    if movement.tempo_bpm == 82: num_segs = [9]
    if movement.tempo_bpm == 84: num_segs = [9, 10]
    if movement.tempo_bpm == 86: num_segs = [9, 10]
    if movement.tempo_bpm == 88: num_segs = [9, 10]
    if movement.tempo_bpm == 90: num_segs = [9, 10]
    if movement.tempo_bpm == 92: num_segs = [10, 11]
    if movement.tempo_bpm == 94: num_segs = [10, 11]
    if movement.tempo_bpm == 96: num_segs = [10, 11]
    if movement.tempo_bpm == 98: num_segs = [10, 11]
    if movement.tempo_bpm == 100: num_segs = [10, 11]
    if movement.tempo_bpm == 102: num_segs = [11, 12]
    if movement.tempo_bpm == 104: num_segs = [11, 12]

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
        4: [
            ['A','B','A','C'],['A','B','A','C'],['A','B','A','C'],['A','B','A','C'],
            ['A','B','C','A'],['A','B','C','A'],['A','B','C','A'], 
            ['A','B','C','B'],['A','B','C','B'],['A','B','C','B'],
            ['A','B','C','C'],['A','B','C','C'],['A','B','C','C'],
            ['A','A','B','C'],['A','A','B','C'],['A','A','B','C'],
            ['A','B','B','C'],['A','B','B','C'],['A','B','B','C'],
            ['A','B','A','C'],['A','B','A','C'],['A','B','A','C'],['A','B','A','C'],
            ['A','B','C','A'],['A','B','C','A'],['A','B','C','A'], 
            ['A','B','C','B'],['A','B','C','B'],['A','B','C','B'],
            ['A','B','C','C'],['A','B','C','C'],['A','B','C','C'],
            ['A','A','B','C'],['A','A','B','C'],['A','A','B','C'],
            ['A','B','B','C'],['A','B','B','C'],['A','B','B','C'],
            
            ['A','A','A','A'],['A','A','B','A'],['A','A','B','B'],
            ['A','A','A','B'],['A','B','B','B'],
            ['A','B','B','A'],['A','B','A','A']
        ]
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
    section_type.num_of_segments = random.choice([1,1,1,2,2,4])
    section_type.segment_order = random.choice(movement.subsegment_order_options[section_type.num_of_segments])
    section_type.segment_type_names = list(set(section_type.segment_order))    
    movement.segment_types[name] = section_type 
    section_type.segment_types = {}
    section_type.schizoid_harmony = movement.schizoid_harmony
    make_harmony_options(section_type)

    section_type.register = {}
    make_keyboard_registers(section_type)
    make_keyboard_thickness(section_type)
    make_guitar_registers(section_type)
    section_type.soprano_start_pitch = random.choice(range(6,13))
    
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
    phrase_type.register = {}
    phrase_type.rhythm = {}
    for musician in phrase_type.movement.musicians:
        phrase_type.notes[musician.name] = []
        phrase_type.movement.notes[musician.name] = []

    make_keyboard_parts(phrase_type)
    make_guitar_parts(phrase_type)
    make_soprano_parts(phrase_type)
    make_guitarists_vocals(phrase_type)
    make_keyboardists_vocals(phrase_type)
    make_horns_or_backing_vocals(phrase_type)

#---------------------------------------    
def make_measures(segment):
    segment.measures = []
    s = 0
    for x in range(segment.duration/16):
        m = BaseEvent(start=s, duration=16)
        m.time_signature = (4,4)
        s += 16
        segment.measures.append(m)

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
    if segment.name == 'I' or segment.name == 'II':
        chordtypes = preferred_chordtypes[4] + preferred_chordtypes[4] + \
                   preferred_chordtypes[3] + \
                   preferred_chordtypes[3] + preferred_chordtypes[3]
    if segment.name == 'III':
        if random.choice([True,False]) == True:
            chordtypes = preferred_chordtypes[3] + preferred_chordtypes[3] + \
                       preferred_chordtypes[3] + preferred_chordtypes[2]
        else:
            chordtypes = preferred_chordtypes[5] + preferred_chordtypes[4] + \
                       preferred_chordtypes[4] + \
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
        #print harmony.pitches
        root_change, harmony.chordtype = get_chordtype(harmony.pitches)
        harmony.root = (harmony.pitches[0] + root_change) % 12
        #print harmony.root, harmony.chordtype
        harmony.sharps_or_flats = chordSharpsOrFlats(list(harmony.pitches), prev_sharps_or_flats)        
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
def make_keyboardists_vocals(segment):
    make_keyboardists_vocals_notes(segment, 'QuentinVoice', 'Quentin')
    make_keyboardists_vocals_notes(segment, 'PhilVoice', 'Phil')
    
def make_keyboardists_vocals_notes(segment, m_voice, m_keyboard):
    segment.movement.notes[m_voice] = []
    segment.notes[m_voice] = []
    prev_pitch = -8
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    s = segment.start
    counter = 0
    for old in segment.notes[m_keyboard]:
        n = Event(start=s, duration=old.duration)
        s += n.duration
        if n.start == segment.start:
            n.rehearsal = True
            n.rehearsal_type = 'plain'
            n.rehearsal_text = rehearsal_text        
        harmony = get_at_microbeat(n.start, segment.harmonies)
        harmony = harmony[0]
        n.sharps_or_flats = harmony.sharps_or_flats 
            
        if counter % 3 == 1 and m_voice == 'QuentinVoice':
            n.pitches = []
        elif counter % 3 == 2 and m_voice == 'PhilVoice':
            n.pitches = []
        else:           
            
            register = segment.movement.musicians_by_name[m_voice].instrument.register
            secondary_pitch_opts = []
            tertiary_pitch_opts = []
            keyboard_pitches_in_register = list(set(old.pitches) & set(register))
            keyboard_pitchclasses = [x % 12 for x in old.pitches]
            keyboard_pitchclasses_in_register = [x for x in register if x%12 in keyboard_pitchclasses]
            if keyboard_pitches_in_register:
                if prev_pitch in keyboard_pitches_in_register:
                    chosen_pitch = prev_pitch
                else:
                    if prev_pitch+1 in keyboard_pitches_in_register:
                        secondary_pitch_opts.append(prev_pitch+1)
                    if prev_pitch+2 in keyboard_pitches_in_register:
                        secondary_pitch_opts.append(prev_pitch+2)            
                    if prev_pitch-1 in keyboard_pitches_in_register:
                        secondary_pitch_opts.append(prev_pitch-1)
                    if prev_pitch-2 in keyboard_pitches_in_register:
                        secondary_pitch_opts.append(prev_pitch-2)
                    if secondary_pitch_opts:
                        chosen_pitch = random.choice(secondary_pitch_opts)
                    else:
                        chosen_pitch = random.choice(keyboard_pitches_in_register)
            else:
                if prev_pitch in keyboard_pitchclasses_in_register:                
                    chosen_pitch = prev_pitch
                else:
                    if prev_pitch+1 in keyboard_pitchclasses_in_register:
                        secondary_pitch_opts.append(prev_pitch+1)
                    if prev_pitch+2 in keyboard_pitchclasses_in_register:
                        secondary_pitch_opts.append(prev_pitch+2)            
                    if prev_pitch-1 in keyboard_pitchclasses_in_register:
                        secondary_pitch_opts.append(prev_pitch-1)
                    if prev_pitch-2 in keyboard_pitchclasses_in_register:
                        secondary_pitch_opts.append(prev_pitch-2)
                    if secondary_pitch_opts:
                        chosen_pitch = random.choice(secondary_pitch_opts)
                    else:
                        chosen_pitch = random.choice(keyboard_pitchclasses_in_register)
            n.pitches = [chosen_pitch]
            
            lyric_opts = ['ooh', 'ah']
            lyric = random.choice(lyric_opts)
            n.lyric = lyric
        segment.notes[m_voice].append(n)
        counter += 1

#---------------------------------------
def make_guitarists_vocals(segment):
    make_guitarist_vocals_notes(segment, 'MattVoice', 'Matt')
    make_guitarist_vocals_notes(segment, 'IanVoice', 'Ian')
    
def make_guitarist_vocals_notes(segment, m_voice, m_guitar):
    segment.movement.notes[m_voice] = []
    segment.notes[m_voice] = []
    prev_pitch = -8
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    s = segment.start    
    for old in segment.notes[m_guitar]:
        n = Event(start=s, duration=old.duration)
        s += n.duration
        if n.start == segment.start:
            n.rehearsal = True
            n.rehearsal_type = 'plain'
            n.rehearsal_text = rehearsal_text        
        if old.pitches == []:
            n.pitches = []
        else:
            
            harmony = get_at_microbeat(n.start, segment.harmonies)
            harmony = harmony[0]
            n.sharps_or_flats = harmony.sharps_or_flats            
            
            register = segment.movement.musicians_by_name[m_voice].instrument.register
            secondary_pitch_opts = []
            tertiary_pitch_opts = []
            guitar_pitches_in_register = list(set(old.pitches) & set(register))
            guitar_pitchclasses = [x % 12 for x in old.pitches]
            guitar_pitchclasses_in_register = [x for x in register if x%12 in guitar_pitchclasses]
            if guitar_pitches_in_register:
                if prev_pitch in guitar_pitches_in_register:
                    chosen_pitch = prev_pitch
                else:
                    if prev_pitch+1 in guitar_pitches_in_register:
                        secondary_pitch_opts.append(prev_pitch+1)
                    if prev_pitch+2 in guitar_pitches_in_register:
                        secondary_pitch_opts.append(prev_pitch+2)            
                    if prev_pitch-1 in guitar_pitches_in_register:
                        secondary_pitch_opts.append(prev_pitch-1)
                    if prev_pitch-2 in guitar_pitches_in_register:
                        secondary_pitch_opts.append(prev_pitch-2)
                    if secondary_pitch_opts:
                        chosen_pitch = random.choice(secondary_pitch_opts)
                    else:
                        chosen_pitch = random.choice(guitar_pitches_in_register)
            else:
                if prev_pitch in guitar_pitchclasses_in_register:                
                    chosen_pitch = prev_pitch
                else:
                    if prev_pitch+1 in guitar_pitchclasses_in_register:
                        secondary_pitch_opts.append(prev_pitch+1)
                    if prev_pitch+2 in guitar_pitchclasses_in_register:
                        secondary_pitch_opts.append(prev_pitch+2)            
                    if prev_pitch-1 in guitar_pitchclasses_in_register:
                        secondary_pitch_opts.append(prev_pitch-1)
                    if prev_pitch-2 in guitar_pitchclasses_in_register:
                        secondary_pitch_opts.append(prev_pitch-2)
                    if secondary_pitch_opts:
                        chosen_pitch = random.choice(secondary_pitch_opts)
                    else:
                        chosen_pitch = random.choice(guitar_pitchclasses_in_register)
            n.pitches = [chosen_pitch]
            
            lyric_opts = ['ooh', 'ah']
            lyric = random.choice(lyric_opts)
            n.lyric = lyric
        segment.notes[m_voice].append(n) 


#---------------------------------------
def make_soprano_parts(segment):
    sopranos = ['Erin', 'Laura']
    make_soprano_rhythms(segment)
    segment.soprano_start_pitch = segment.section_type.soprano_start_pitch 
    for m in sopranos:
        segment.register[m] = segment.movement.musicians_by_name[m].instrument.register
        make_soprano_notes(segment, m)

def make_soprano_notes(segment, m):
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    segment.movement.notes[m] = []
    prev_pitch = segment.soprano_start_pitch
    prev_direction = ['+', '+', '+']
    s = segment.start
    for r in segment.rhythm[m]:
        note = Event(duration=r.duration, start=s)
        s += note.duration
        if note.start == segment.start:
            note.rehearsal = True
            note.rehearsal_type = 'plain'
            note.rehearsal_text = rehearsal_text        
        if not r.rest:
            note.pitches = []
        else:      
            harmony = get_at_microbeat(note.start, segment.harmonies)
            harmony = harmony[0]
            note.sharps_or_flats = harmony.sharps_or_flats
            pitch_options = [p for p in segment.register[m] if p%12 in harmony.pitches]
            preferred_pitches = []
            secondary_pitches = []
            tertiary_pitches = []
            if prev_pitch in pitch_options: tertiary_pitches.append(prev_pitch)
            if prev_pitch + 1 in pitch_options: preferred_pitches.append(prev_pitch+1)
            if prev_pitch + 2 in pitch_options: preferred_pitches.append(prev_pitch+2)
            if prev_pitch + 3 in pitch_options: preferred_pitches.append(prev_pitch + 3)
            if prev_pitch + 4 in pitch_options: secondary_pitches.append(prev_pitch + 4)
            if prev_pitch + 5 in pitch_options: secondary_pitches.append(prev_pitch + 5)
            if prev_pitch + 6 in pitch_options: tertiary_pitches.append(prev_pitch + 6)
            if prev_pitch + 7 in pitch_options: tertiary_pitches.append(prev_pitch + 7)            
            if prev_pitch - 1 in pitch_options: preferred_pitches.append(prev_pitch-1)
            if prev_pitch - 2 in pitch_options: preferred_pitches.append(prev_pitch-2)
            if prev_pitch - 3 in pitch_options: preferred_pitches.append(prev_pitch - 3)
            if prev_pitch - 4 in pitch_options: secondary_pitches.append(prev_pitch - 4)        
            if prev_pitch - 5 in pitch_options: secondary_pitches.append(prev_pitch - 5)
            if prev_pitch - 6 in pitch_options: tertiary_pitches.append(prev_pitch - 6)
            if prev_pitch - 7 in pitch_options: tertiary_pitches.append(prev_pitch - 7)     
            
            if preferred_pitches:
                chosen_pitch = random.choice(preferred_pitches)
            elif secondary_pitches:
                chosen_pitch = random.choice(secondary_pitches)
            elif tertiary_pitches:
                chosen_pitch = random.choice(tertiary_pitches)          
            else:
                chosen_pitch = random.choice(pitch_options)                       
            note.pitches = [chosen_pitch]
            prev_pitch = chosen_pitch
            
            lyric_opts = ['ah', 'ah', 'ah', 'ooh', 'ooh', 'oh', 'ee', 'ee']
            lyric = random.choice(lyric_opts)
            note.lyric = lyric
        
        segment.notes[m].append(note) 
    
        
def make_soprano_rhythms(segment):
    if segment.section_type.name == 'I' or segment.section_type.name == 'II':
        opts_A = [
            [(True,12),(True,4)],
            [(True,12),(True,4)],
            [(True,12),(True,2),(True,2)],
            [(True,12),(True,3),(True,1)],
            [(True,7),(True,1),(True,8)],
            [(True,6),(True,2),(True,8)],        
            [(True,4),(True,4),(True,8)],
            [(True,8),(True,4),(True,4)],
            [(True,3),(True,1),(True,12)],
            [(True,4),(True,12)],            
            [(True,16)],
            [(True,8),(True,8)],
            [(True,4),(True,12)],            
            [(True,16)],
            [(True,8),(True,8)],
            [(True,8),(True,7),(True,1)],
            [(True,4),(True,8),(True,4)]
        ]
        opts_B = [
            [(True,8),(False,8)],
            [(False,8),(True,8)],
            [(True,12),(False,4)],
            [(True,4),(False,12)],
            [(False,12),(True,4)],
            [(False,4),(True,12)],
            [(True,4),(False,8),(True,4)],
            [(True,4),(False,4),(True,8)]
        ]
    if segment.section_type.name == 'III':
        opts_A = [
            [(True,4),(True,4),(True,4),(True,4)],
            [(True,4),(True,4),(True,4),(True,2),(True,2)],
            [(True,4),(True,4),(True,4),(True,3),(True,1)],
            [(True,4),(True,4),(True,4),(True,2),(True,1),(True,1)],        
            [(True,4),(True,4),(True,4),(True,1),(True,1),(True,1),(True,1)], 
            [(True,4),(True,4),(True,4),(True,1),(True,1),(True,2)],
            [(True,12),(True,4)],
            [(True,12),(True,2),(True,2)],
            [(True,12),(True,3),(True,1)],
            [(True,12),(True,2),(True,1),(True,1)],        
            [(True,12),(True,1),(True,1),(True,1),(True,1)], 
            [(True,12),(True,1),(True,1),(True,2)],
            [(True,7),(True,1),(True,8)],
            [(True,6),(True,2),(True,8)],        
            [(True,4),(True,4),(True,8)],
            [(True,8),(True,4),(True,4)],         
            [(True,8),(True,4),(True,1),(True,1),(True,1),(True,1)], 
            [(True,1),(True,1),(True,1),(True,1),(True,8),(True,4)],
            [(True,3),(True,1),(True,3),(True,1),(True,3),(True,1),(True,4)],
            [(True,3),(True,1),(True,12)],
            [(True,1),(True,1),(True,2),(True,4),(True,8)],
            [(True,4),(True,4),(True,1),(True,1),(True,1),(True,1),(True,4)]
        ]
        opts_B = [
            [(True,8),(False,8)],
            [(True,12),(False,4)],
            [(True,4),(False,12)],
            [(True,3),(True,1),(True,4),(False,8)],
            [(True,1),(True,1),(True,1),(True,1),(True,4),(False,8)],
            [(True,4),(True,4),(True,4),(False,4)],
            [(True,4),(True,4),(True,4),(False,4)],
            [(True,4),(False,8),(True,4)],
            [(True,4),(False,8),(True,2),(True,2)],        
            [(True,4),(False,8),(True,3),(True,1)],
            [(True,4),(False,8),(True,2),(True,1),(True,1)],
            [(True,4),(False,8),(True,1),(True,1),(True,2)],
            [(True,4),(False,8),(True,1),(True,1),(True,2)],    
            [(True,4),(False,8),(True,1),(True,1),(True,1),(True,1)],    
            [(True,4),(False,4),(True,8)],
            [(True,4),(False,4),(True,4),(True,4)],
            [(True,4),(False,4),(True,4),(True,2),(True,2)]
        ]
    
    num_bars = segment.duration/16
    segment.rhythm['Erin'] = []
    segment.rhythm['Laura'] = []
    s1 = segment.start
    s2 = segment.start
    for b in range(num_bars):
        if b % 2 == 0: # even
            erin_rhythm = random.choice(opts_A)
            laura_rhythm = random.choice(opts_B)
        else:
            erin_rhythm = random.choice(opts_B)
            laura_rhythm = random.choice(opts_A)        
        
        for e in erin_rhythm:
            r = BaseEvent(start=s1, duration=e[1])
            r.rest = e[0]
            segment.rhythm['Erin'].append(r)
            s1 += r.duration
        for l in laura_rhythm:
            q = BaseEvent(start=s2, duration=l[1])
            q.rest = l[0]
            segment.rhythm['Laura'].append(q)
            s2 += q.duration        
  
            
#---------------------------------------
def make_guitar_parts(segment):
    guitarists = ['Matt', 'Ian']
    make_guitar_rhythms(segment)
    for m in guitarists:
        segment.register[m] = segment.section_type.register[m]
        make_guitar_notes(segment, m)

def make_guitar_rhythms(segment):
    opts = [
        [(True,16)],
        [(False,16)],
        [(True,8),(False,8)],
        [(False,8),(True,8)],        
        [(True,12),(True,4)],
        [(True,12),(True,4)],
        [(True,8),(True,8)],
        [(True,8),(True,4),(True,4)],
        [(True,16)],
        [(False,16)],
        [(True,16)],
        [(False,16)],
        [(False,16)]        
    ]
    num_bars = segment.duration/16
    segment.guitar_rhythms = []
    s = segment.start
    for b in range(num_bars):   
        rhythm = random.choice(opts)
        for e in rhythm:
            r = BaseEvent(start=s, duration=e[1])
            r.rest = e[0]
            segment.guitar_rhythms.append(r)
            s += r.duration

def make_guitar_notes(segment, m):
    segment.movement.notes[m] = []
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    s = segment.start
    for r in segment.guitar_rhythms:
        n = Event(start=s, duration=r.duration)
        s += n.duration
        if n.start == segment.start:
            n.rehearsal = True
            n.rehearsal_type = 'plain'
            n.rehearsal_text = rehearsal_text        
        if not r.rest:
            n.pitches = []
            segment.notes[m].append(n)
        else:
            harmony = get_at_microbeat(n.start, segment.harmonies)
            harmony = harmony[0]
            n.sharps_or_flats = harmony.sharps_or_flats
            chord_options = get_fingerings_by_root_chordtype_range(
                harmony.root, 
                harmony.chordtype,
                segment.register[m][0],
                segment.register[m][-1]
            )
            n.fretboard_diagram, n.pitches = random.choice(chord_options)
            segment.notes[m].append(n)
  
def make_guitar_registers(segment):
    guitarists = ['Matt', 'Ian']
    for m in guitarists:       
        max_register = segment.movement.musicians_by_name[m].instrument.register
        lo = weighted_choice(range(-20,-12), range(1,9))
        hi = weighted_choice(range(11, 17), range(6,0,-1))
        segment.register[m] = range(lo, hi+1) 
    
#---------------------------------------
def make_keyboard_parts(segment):
    keyboardists = ['Quentin', 'Phil', 'Will']
    segment.keyboard_thickness = {}    
    for m in keyboardists:       
        segment.rhythm[m] = segment.harmonic_rhythm
        segment.register[m] = segment.section_type.register[m]
        segment.keyboard_thickness[m] = segment.section_type.keyboard_thickness[m]
        make_keyboard_notes(segment, m)

def make_keyboard_registers(segment):
    keyboardists = ['Quentin', 'Phil', 'Will']
    for m in keyboardists:       
        max_register = segment.movement.musicians_by_name[m].instrument.register
        width = random.choice(range(19,32))       
        highest_low_note = max_register[-1] - width
        low_note_opts = range(max_register[0], highest_low_note)
        if len(low_note_opts) % 2 == 0: # even            
            weights_lo = range(1, (len(low_note_opts)/2)+1)
            weights_hi = range((len(low_note_opts)/2), 0, -1)
        if len(low_note_opts) % 2 == 1: # odd            
            weights_lo = range(1, (len(low_note_opts)/2)+1)
            weights_hi = range((len(low_note_opts)/2)+1, 0, -1)            
        weights = weights_lo + weights_hi
        low = weighted_choice(low_note_opts, weights)
        segment.register[m] = range(low, low + width)
        
def make_keyboard_thickness(segment):
    keyboardists = ['Quentin', 'Phil', 'Will']
    segment.keyboard_thickness = {}
    for m in keyboardists:
        segment.keyboard_thickness[m] = range(random.choice(range(1,4)), random.choice(range(5,9)))
 
def make_keyboard_notes(segment, m):
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    segment.movement.notes[m] = []
    s = segment.start
    for d in segment.rhythm[m]:
        note = Event(duration=d, start=s)
        if note.start == segment.start:
            note.rehearsal = True
            note.rehearsal_type = 'plain'
            note.rehearsal_text = rehearsal_text
        s += d
        harmony = get_at_microbeat(note.start, segment.harmonies)
        harmony = harmony[0]
        note.sharps_or_flats = harmony.sharps_or_flats
        pitch_options = [p for p in segment.register[m] if p%12 in harmony.pitches]
        num_notes = random.choice(segment.keyboard_thickness[m])
        note.pitches = []
        for n in range(num_notes):
            p = random.choice(pitch_options)
            if p not in note.pitches:
                note.pitches.append(p)
            else:
                p = random.choice(pitch_options)
                if p not in note.pitches:
                    note.pitches.append(p)
        segment.notes[m].append(note)

#---------------------------------------

def make_horns_or_backing_vocals(segment):
    horn_players = ['Katie', 'Beth', 'Jason']
    if segment.section_type.name not in segment.movement.sections_with_horns:
        for m in horn_players:
            segment.notes[m] = []
            num_bars = segment.duration/16
            s = segment.start
            for b in range(num_bars):
                e = Event(start=s, duration=16)
                s += e.duration
                e.pitches = []
                segment.notes[m].append(e)
    else:
        lead, backup_duo = make_horn_vocal_rhythm(segment)
        if segment.movement.horns:
            make_horns_parts(segment, backup_duo, 'Katie')
            make_horns_parts(segment, backup_duo, 'Beth')
            make_horns_parts(segment, lead, 'Jason')
        else:
            make_backing_vocals(segment, lead, 'Katie')
            make_backing_vocals(segment, backup_duo, 'Beth')
            make_backing_vocals(segment, backup_duo, 'Jason')
            
def make_horn_vocal_rhythm(segment):
    opts_A = [
        [(True,12),(True,4)],
        [(True,12),(True,4)],
        [(True,12),(True,2),(True,2)],
        [(True,12),(True,3),(True,1)],
        [(True,7),(True,1),(True,8)],
        [(True,6),(True,2),(True,8)],        
        [(True,4),(True,4),(True,8)],
        [(True,8),(True,4),(True,4)],
        [(True,3),(True,1),(True,12)],
        [(True,4),(True,12)],            
        [(True,16)],
        [(True,8),(True,8)],
        [(True,4),(True,12)],            
        [(True,16)],
        [(True,8),(True,8)],
        [(True,8),(True,7),(True,1)],
        [(True,4),(True,8),(True,4)]
    ]
    opts_B = [
        [(True,8),(False,8)],
        [(False,8),(True,8)],
        [(True,12),(False,4)],
        [(True,4),(False,12)],
        [(False,12),(True,4)],
        [(False,4),(True,12)],
        [(True,4),(False,8),(True,4)],
        [(True,4),(False,4),(True,8)]
    ]
    num_bars = segment.duration/16
    lead = []
    backup_duo = []
    s1 = segment.start
    s2 = segment.start
    for b in range(num_bars):
        if b % 2 == 0: # even
            lead_rhythm = random.choice(opts_A)
            backup_duo_rhythm = random.choice(opts_B)
        else:
            lead_rhythm = random.choice(opts_B)
            backup_duo_rhythm = random.choice(opts_A)        
        
        for e in lead_rhythm:
            r = BaseEvent(start=s1, duration=e[1])
            r.rest = e[0]
            lead.append(r)
            s1 += r.duration
        for l in backup_duo_rhythm:
            q = BaseEvent(start=s2, duration=l[1])
            q.rest = l[0]
            backup_duo.append(q)
            s2 += q.duration
    return lead, backup_duo
    
def make_horns_parts(segment, rhythm, m):
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    segment.movement.notes[m] = []
    register = segment.movement.musicians_by_name[m].instrument.register
    prev_pitch = register[len(register)/2]
    s = segment.start
    for r in rhythm:
        note = Event(duration=r.duration, start=s)
        s += note.duration
        if note.start == segment.start:
            note.rehearsal = True
            note.rehearsal_type = 'plain'
            note.rehearsal_text = rehearsal_text        
        if not r.rest:
            note.pitches = []
        else:      
            harmony = get_at_microbeat(note.start, segment.harmonies)
            harmony = harmony[0]
            note.sharps_or_flats = harmony.sharps_or_flats
            pitch_options = [p for p in register if p%12 in harmony.pitches]
            preferred_pitches = []
            secondary_pitches = []
            tertiary_pitches = []
            if prev_pitch in pitch_options: preferred_pitches.append(prev_pitch)
            if prev_pitch + 1 in pitch_options: preferred_pitches.append(prev_pitch+1)
            if prev_pitch + 2 in pitch_options: preferred_pitches.append(prev_pitch+2)
            if prev_pitch + 3 in pitch_options: secondary_pitches.append(prev_pitch + 3)
            if prev_pitch + 4 in pitch_options: secondary_pitches.append(prev_pitch + 4)
            if prev_pitch + 5 in pitch_options: tertiary_pitches.append(prev_pitch + 5)
            if prev_pitch + 6 in pitch_options: tertiary_pitches.append(prev_pitch + 6)
            if prev_pitch + 7 in pitch_options: tertiary_pitches.append(prev_pitch + 7)            
            if prev_pitch - 1 in pitch_options: preferred_pitches.append(prev_pitch-1)
            if prev_pitch - 2 in pitch_options: preferred_pitches.append(prev_pitch-2)
            if prev_pitch - 3 in pitch_options: secondary_pitches.append(prev_pitch - 3)
            if prev_pitch - 4 in pitch_options: secondary_pitches.append(prev_pitch - 4)        
            if prev_pitch - 5 in pitch_options: tertiary_pitches.append(prev_pitch - 5)
            if prev_pitch - 6 in pitch_options: tertiary_pitches.append(prev_pitch - 6)
            if prev_pitch - 7 in pitch_options: tertiary_pitches.append(prev_pitch - 7)     
            
            if preferred_pitches:
                chosen_pitch = random.choice(preferred_pitches)
            elif secondary_pitches:
                chosen_pitch = random.choice(secondary_pitches)
            elif tertiary_pitches:
                chosen_pitch = random.choice(tertiary_pitches)          
            else:
                chosen_pitch = random.choice(pitch_options)                       
            note.pitches = [chosen_pitch]
            prev_pitch = chosen_pitch
        
        segment.notes[m].append(note)

def make_backing_vocals(segment, rhythm, m):
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    segment.movement.notes[m] = []
    register = segment.movement.musicians_by_name[m].instrument.register
    prev_pitch = register[len(register)/2]
    s = segment.start
    for r in rhythm:        
        note = Event(duration=r.duration, start=s)
        s += note.duration
        if note.start == segment.start:
            note.rehearsal = True
            note.rehearsal_type = 'plain'
            note.rehearsal_text = rehearsal_text        
        if not r.rest:
            note.pitches = []
        else:      
            harmony = get_at_microbeat(note.start, segment.harmonies)
            harmony = harmony[0]
            note.sharps_or_flats = harmony.sharps_or_flats
            pitch_options = [p for p in register if p%12 in harmony.pitches]
            preferred_pitches = []
            secondary_pitches = []
            tertiary_pitches = []
            if prev_pitch in pitch_options: preferred_pitches.append(prev_pitch)
            if prev_pitch + 1 in pitch_options: preferred_pitches.append(prev_pitch+1)
            if prev_pitch + 2 in pitch_options: preferred_pitches.append(prev_pitch+2)
            if prev_pitch + 3 in pitch_options: secondary_pitches.append(prev_pitch + 3)
            if prev_pitch + 4 in pitch_options: secondary_pitches.append(prev_pitch + 4)
            if prev_pitch + 5 in pitch_options: tertiary_pitches.append(prev_pitch + 5)
            if prev_pitch + 6 in pitch_options: tertiary_pitches.append(prev_pitch + 6)
            if prev_pitch + 7 in pitch_options: tertiary_pitches.append(prev_pitch + 7)            
            if prev_pitch - 1 in pitch_options: preferred_pitches.append(prev_pitch-1)
            if prev_pitch - 2 in pitch_options: preferred_pitches.append(prev_pitch-2)
            if prev_pitch - 3 in pitch_options: secondary_pitches.append(prev_pitch - 3)
            if prev_pitch - 4 in pitch_options: secondary_pitches.append(prev_pitch - 4)        
            if prev_pitch - 5 in pitch_options: tertiary_pitches.append(prev_pitch - 5)
            if prev_pitch - 6 in pitch_options: tertiary_pitches.append(prev_pitch - 6)
            if prev_pitch - 7 in pitch_options: tertiary_pitches.append(prev_pitch - 7)     
            
            if preferred_pitches:
                chosen_pitch = random.choice(preferred_pitches)
            elif secondary_pitches:
                chosen_pitch = random.choice(secondary_pitches)
            elif tertiary_pitches:
                chosen_pitch = random.choice(tertiary_pitches)          
            else:
                chosen_pitch = random.choice(pitch_options)                       
            note.pitches = [chosen_pitch]
            prev_pitch = chosen_pitch
            
            lyric_opts = ['ah', 'ah', 'ah', 'ooh', 'ooh', 'ee', 'ee']
            lyric = random.choice(lyric_opts)
            note.lyric = lyric
        
        segment.notes[m].append(note)

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

##    print '^'*15
##    for m in ['Matt', 'Ian']:
##        print m
##        for section in movement.segments:
##            for phrase in section.segments:
##                for n in phrase.notes[m]:
##                    print n.start, n.duration
##    print '+'*15    
    
        
def put_notes_in_movement(movement):
    for section in movement.segments:
        for phrase in section.segments:
            movement.measures.extend(phrase.measures)
            movement.harmonies.extend(phrase.harmonies)
            for musician in movement.musicians:
                movement.notes[musician.name].extend(phrase.notes[musician.name])
##    for m in ['Quentin', 'Phil', 'Will']:
##        print m
##        for n in movement.notes[m]:
##            print n.start, n.duration, '*'*8
 
def make_report(movement):
    a = 'tempo: {0}\n'.format(movement.tempo_bpm)
    b = 'duration in sixteenth notes: {0}\n'.format(movement.duration)
    c = 'duration in seconds: {0}\n'.format(movement.duration_seconds)
    x = 'schizoid harmony: {0}\n'.format(movement.schizoid_harmony)
    movement.report = [a,b,c,x]
    double_line = '='*40
    single_line = '-'*20
    for section in movement.segments:
        d = '{0:<5}{1}\n'.format(section.name, double_line)
        movement.report.append(d)
        for phrase in section.segments:
            e = '{0:<5}{1}\n'.format(phrase.name, single_line)
            movement.report.append(e)
            for r, h in zip(phrase.harmonic_rhythm, phrase.harmonies):
                f = '\t{0:<5}{1}\n'.format(r, h.pitches)
                movement.report.append(f)
    movement.report = ''.join(movement.report)
    print movement.report


#---------------------------------------
def main(mv_type):
    movement = make_movement(mv_type)
    make_phrases(movement)
    make_sections(movement)
    put_notes_in_movement(movement)
    make_report(movement)
    return movement

class MvmtType3(BaseMovement):
    def __init__(self, piece, movement_name, seq_number, folder_name, file_name_prefix, main_title, subtitle):
        self.folder_name = folder_name
        self.file_name_prefix = file_name_prefix
        self.main_title = main_title
        self.subtitle = subtitle
        BaseMovement.__init__(self, piece, movement_name, seq_number)        

        self.horns = random.choice([True, False])
        self.choose_ensemble()
        
        movement = main(self)
        self.write_file(movement.report, 'form.txt')
        
        self.tempo_duration = 4
        self.tempo_bpm = movement.tempo_bpm
        self.duration_denominator = 16
        


        #for phrase in movement.phrases:
        self.musicians_by_name['Erin'].music.extend(movement.notes['Erin'])
        self.musicians_by_name['Laura'].music.extend(movement.notes['Laura'])
        self.musicians_by_name['QuentinVoice'].music.extend(movement.notes['QuentinVoice'])
        self.musicians_by_name['Quentin'].music.extend(movement.notes['Quentin'])
        self.musicians_by_name['PhilVoice'].music.extend(movement.notes['PhilVoice'])
        self.musicians_by_name['Phil'].music.extend(movement.notes['Phil'])
        self.musicians_by_name['Will'].music.extend(movement.notes['Will'])
        self.musicians_by_name['MattVoice'].music.extend(movement.notes['MattVoice'])
        self.musicians_by_name['Matt'].music.extend(movement.notes['Matt'])    
        self.musicians_by_name['IanVoice'].music.extend(movement.notes['IanVoice'])
        self.musicians_by_name['Ian'].music.extend(movement.notes['Ian']) 
        self.musicians_by_name['Katie'].music.extend(movement.notes['Katie'])
        self.musicians_by_name['Beth'].music.extend(movement.notes['Beth'])
        self.musicians_by_name['Jason'].music.extend(movement.notes['Jason'])

        self.make_meter(movement)
        BaseMovement.ly_closeout(self)

    def choose_ensemble(self):
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

        keyboard_instrument = random.choice(sustaining_keyboard_options)
        will = Musician(midi_instruments[keyboard_instrument])
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

        if self.horns == True:        
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
        s = 0
        for measure in movement.measures:
            m = Measure(measure.time_signature[0], measure.time_signature[1], self.duration_denominator, s)
            self.measures.append(m)
            s = m.next_measure_start


##if __name__ == '__main__':
##    main()











