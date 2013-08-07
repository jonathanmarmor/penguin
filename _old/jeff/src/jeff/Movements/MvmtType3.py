import random
import itertools
from piece.BaseEvent import Event, BaseEvent
from piece.pitches import chordSharpsOrFlats
from piece.common_combinations import thirtytwo, sixtyfour
from piece.chordtypes import get_chordtype
from piece.BaseMovement import BaseMovement, Musician
from piece.measure import Measure
from piece.instruments import Guitar, SopranoSaxophone, Trumpet, CasioSK1, \
    Piano, Bass, Flute

from Movements.Mvmt3_make_ensembles import make_ensembles
from Movements.MvmtType5_chordtypes import preferred_chordtypes, chords_scales

from piece.weighted_choice import weighted_choice
from Movements.divide_into_4 import divide_into_4
from Movements.build_chord_options import chordtypes_on_roots, containing, chords_in_scale, get_scales_containing_chord
from Movements.dogstar_chord_rhythms import get_chord_rhythm

from piece.copy_Event import deepcopy_Event

def get_at_microbeat(mb, field):
    result = []
    for e in field:
        if mb in e.microbeats:
            result.append(e)
    return result


def main(mv_type):
    movement = make_movement(mv_type)
    phrase_notes_to_musicians(movement)
    
    get_tempo_change_points(movement)
    make_section_dynamics(movement)
    add_gracenotes(movement)
    
##    make_sections(movement)
##    put_notes_in_movement(movement)
    #make_report(movement)
    return movement

def get_tempo_change_points(movement):
    groups = []
    prev = None
    for phrase in movement.phrases:
        if phrase.section_type.name != prev:
            group = [phrase]
            groups.append(group)
            prev = phrase.section_type.name
        else:
            group.append(phrase)
    tempo_messages = choose_tempo_messages()
    get_rall_start(groups)
    get_a_tempo(groups)
    rall_a_tempo_to_music(movement, tempo_messages)

##    for phrases in groups:
##        print phrases[0].section_type.name
##        print phrases[0].start
##        for phrase in phrases:
##            if phrase.a_tempo:
##                print 'a_tempo', phrase.a_tempo
##            if phrase.rall_start:
##                print 'rall_start', phrase.rall_start
##
##        print phrases[-1].end + 1
##        print

    
    
def get_rall_start(groups):
    for phrases in groups:
        start_opts = phrases[0].start + ((phrases[-1].end + 1 - phrases[0].start)/8)*5
        opts = range(start_opts, phrases[-1].end + 2)
        rall_start = random.choice(opts)
        for phrase in phrases:
            if rall_start >= phrase.start and rall_start <= phrase.end:
                phrase.rall_start = rall_start
            else:
                phrase.rall_start = None

            
def get_a_tempo(groups):
    for phrase in groups[0]:
        phrase.a_tempo = None
    for phrases in groups[1:]:        
        end_opts = phrases[0].start + ((phrases[-1].end + 1 - phrases[0].start)/8)*2
        opts = range(phrases[0].start, end_opts + 1)
        a_tempo = random.choice(opts)
        for phrase in phrases:
            if a_tempo >= phrase.start and a_tempo <= phrase.end:
                phrase.a_tempo = a_tempo
            else:
                phrase.a_tempo = None
            

def choose_tempo_messages():
    rall_msg_opts = [
        'rall...', 'rall...', 'rall...', 'rall...', 'rall...', 
        'acc...'
    ]
    a_tempo_msg_opts = [
        'a tempo', 'a tempo', 'a tempo',
        'a tempo but a little slower',
        'a tempo but a little faster',
    ]
    d = {
        'I': {
            'rall':random.choice(rall_msg_opts),
            'a_tempo':random.choice(a_tempo_msg_opts)
        },
    'II': {
            'rall':random.choice(rall_msg_opts),
            'a_tempo':random.choice(a_tempo_msg_opts)
        },
    'III': {
            'rall':random.choice(rall_msg_opts),
            'a_tempo':random.choice(a_tempo_msg_opts)
        }  
    }
    return d
    


def rall_a_tempo_to_music(movement, tempo_messages):
    for phrase in movement.phrases:
        if phrase.a_tempo:
            a_tempo_msg = tempo_messages[phrase.section_type.name]['a_tempo']
            for m in movement.musicians_names:
                musician = movement.musicians_by_name[m]
                note = get_at_microbeat(phrase.a_tempo, musician.music) 
                note = note[0]
                #note.note_text_position = 'below'
                note.note_text = a_tempo_msg
        
        if phrase.rall_start:
            rall_msg = tempo_messages[phrase.section_type.name]['rall'] 
            for m in movement.musicians_names:
                musician = movement.musicians_by_name[m]
                note = get_at_microbeat(phrase.rall_start, musician.music) 
                note = note[0]
                #note.note_text_position = 'below'
                note.note_text = rall_msg
            
    
def make_section_dynamics(movement):
    groups = []
    prev = None
    for phrase in movement.phrases:
        if phrase.section_type.name != prev:
            group = [phrase]
            groups.append(group)
            prev = phrase.section_type.name
        else:
            group.append(phrase)
            
    dynamics = get_section_dynamics(movement)
    
    for phrases in groups:
        i = phrases[0].start
        for m in movement.musicians_names:
            dynamic_msg = dynamics[phrases[0].section_type.name][m]
            
            musician = movement.musicians_by_name[m]
            note = get_at_microbeat(i, musician.music) 
            note = note[0]
            note.dynamic = dynamic_msg

            
def get_section_dynamics(movement):
    opts = [
##        ['pp', 'p', 'mp'],
##        ['p', 'mp', 'mf'],
##        ['mp', 'mf', 'f']

        ['ppp', 'pp', 'p'],
        ['p', 'mp', 'mf'],
        ['mf', 'f', 'ff']    
    ]
    order_opts = [
        (0,0,1),(0,1,1),(0,0,2),(0,1,2),(0,2,2),(1,1,2),(1,2,2),
        (2,2,1),(2,2,0),(2,1,1),(2,1,0),(2,0,0),(1,1,0),(1,0,0)
    ]
    order = random.choice(order_opts)
    secs = ['I', 'II', 'III']
    d = {}
    for o, s in zip(order, secs):
        d[s] = {}
        for m in movement.musicians_names:
            d[s][m] = random.choice(opts[o])
    return d

#=================
def add_gracenotes(movement):
    
    section_type_instruments = {}
    for stn in movement.segment_type_names:
        if movement.segment_types[stn].ornamented:
            print stn, 'ornamented!'
            section_type_instruments[stn] = choose_gracenote_instruments()
        else:
            section_type_instruments[stn] = []

    for phrase in reversed(movement.phrases):
        instruments = section_type_instruments[phrase.section_type.name]
        for m in instruments:
            musician = movement.musicians_by_name[m]
            start_note = get_at_microbeat(phrase.start, musician.music)[0]
            start_index = musician.music.index(start_note)
            end_note = get_at_microbeat(phrase.end, musician.music)[0]
            end_index = musician.music.index(end_note)            
            add_orns(musician.music, start_index, end_index, movement)
            
def choose_gracenote_instruments():
    weights = {'Emma':100,'Paul':1,'Katie':90,'Christine':100,'Mark':60}
    num_insts = random.choice([1,1,1,2,2,2,2,3,3,3])
    instruments = []
    for x in range(num_insts):
        chosen = weighted_choice(weights.keys(), weights.values())
        del weights[chosen]
        instruments.append(chosen)
    return instruments

def add_orns(notes, start, end, movement):
    indices = range(end, start-1, -1)
    for i in indices:
        if orn_criteria(notes[i]):
            orn_pattern = choose_ornament_type()
            notes[i].grace_notes = get_orn_Events(orn_pattern, notes[i], movement)
            notes[i].grace_on_beat = random.choice([True, False, False, False])

def orn_criteria(note):
    if len(note.pitches) == 1 and note.start != 0:
        if random.choice([True,False]):
            return True
        else:
            return False
    else:
        return False

def choose_ornament_type():
    opts = [
        (-1,), (-1,), (-1,), (-1,), (-1,), (-1,),
        (1,), (1,), (1,), (1,), (1,), (1,), 
        (0,-1), (0,1), (2,1), (-2,-1), (-1,1), (1,-1),
        (0,-1), (0,1), (2,1), (-2,-1), (-1,1), (1,-1),
        (-1,0,-1), (1,0,1), (-1,0,1), (1,0,-1),
        (-1,0,-1), (1,0,1), (-1,0,1), (1,0,-1)        
    ]
    return random.choice(opts)                

def get_orn_Events(orn_pattern, note, movement):
    target_pitch = note.pitches[0]
    harmony = get_at_microbeat(note.start, movement.harmonies)[0]
    scale = harmony.diatonic
    gracenote_pitches = get_gracenote_pitches(target_pitch, scale, orn_pattern)
    return gracenote_pitches

def get_gracenote_pitches(target_pitch, scale, ornament_type):
    gracenotes = []
    all_pitches = range(-48, 49)
    scale = [p for p in all_pitches if p%12 in scale]
    target_index = scale.index(target_pitch)
    for trans in ornament_type:
        grace_index = (target_index + trans) % len(scale)
        gracenote_pitch = scale[grace_index]
        gracenotes.append(gracenote_pitch)
    return gracenotes
#=================
def make_movement(mv_type):
    movement = BaseEvent(start=0)
    movement.musicians_names = ['Emma', 'Paul', 'Katie', 'Christine', 'Michael', 'Mark', 'James']

    movement.measures = []
    movement.harmonies = []
    movement.notes = {}
    movement.tempo_bpm = random.choice(range(54,103,4))
        
    movement.drone_pc = random.choice(range(12))
    drone_oct = random.choice([[-12],[0],[12],[-12,0],[-12,12],[0,12],[-12,0,12]])
    movement.drone_pitches = [o+movement.drone_pc for o in drone_oct]
    set_guitar_rhythm_opts_per_harm(movement)
    movement.schizoid_harmony = random.choice([True, False, False, False, False])
    movement.harmonies_tracker = []
    #movement.horns = mv_type.horns
    #movement.sections_with_horns = random.choice([['III'], ['III'], ['II','III'], ['I','II'], ['II']])
    movement.musicians = mv_type.musicians
    movement.musicians_by_name = mv_type.musicians_by_name
    
##    for m in movement.musicians_names:
##        musician = movement.musicians_by_name[m]
##        i = len(musician.instrument.conservative_register)/2        
##        start_note = musician.instrument.conservative_register[i]
##        musician.prev = [start_note, start_note]
    
    
    choose_sections_order(movement)
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
    make_ensemble_roles(movement)

    movement.ensembles = make_ensembles()
##    make_ensembles(movement)
    
    make_form(movement)
    add_music(movement)
    return movement

def make_form(movement):
    make_section_types(movement)
    make_phrase_types(movement)
    make_phrases(movement)
    #make_ensemble_order(movement)

def add_music(movement):
##    make_movement_settings()
##    make_section_type_settings()
##    make_phrase_type_settings()
##    make_phrase_settings()
    make_parts_on_phrases(movement)
    
def choose_sections_order(movement):
    seg_order_opts = {
        4: [
            ['I', 'I', 'II', 'I'],
            ['I', 'II', 'III', 'II'],
            ['I', 'II', 'III', 'I']
        ],
        5: [
            ['I', 'I', 'II', 'III', 'I'],
            ['I', 'I', 'II', 'III', 'II'],
            ['I', 'II', 'I', 'III', 'I'],
            ['I', 'II', 'I', 'III', 'II'],
            ['I', 'II', 'II', 'III', 'I'],
            ['I', 'II', 'II', 'III', 'II'],
            ['I', 'II', 'III', 'I', 'II'],
            ['I', 'II', 'III', 'II', 'I'],
            ['I', 'II', 'III', 'III', 'I']
        ],
        6: [
            ['I', 'I', 'II', 'I', 'III', 'II'],
            ['I', 'II', 'I', 'II', 'III', 'I'],
            ['I', 'I', 'II', 'I', 'III', 'I'],
            ['I', 'II', 'I', 'II', 'III', 'II'],
            ['I', 'I', 'I', 'II', 'III', 'II'],
            ['I', 'II', 'I', 'III', 'III', 'I'],
            ['I', 'II', 'III', 'II', 'III', 'I']
            ],
        7: [
            ['I', 'I', 'II', 'I', 'III', 'III', 'II'],
            ['I', 'I', 'II', 'I', 'III', 'III', 'I'],
            ['I', 'I', 'I', 'II', 'III', 'III', 'II'],
            ['I', 'II', 'I', 'II', 'III', 'III', 'II'],
            ['I', 'II', 'I', 'II', 'III', 'II', 'I'],
            ['I', 'I', 'II', 'II', 'III', 'III', 'I'],
            ['I', 'I', 'II', 'II', 'III', 'II', 'I'],            
            ['I', 'II', 'I', 'III', 'I', 'II', 'I']        
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
            ['I', 'I', 'II', 'II', 'I', 'I', 'III', 'III', 'II', 'I', 'I']
        ]
    }

    if movement.tempo_bpm == 54: num_segs = random.choice([4, 5])
    if movement.tempo_bpm == 58: num_segs = random.choice([4, 5])
    if movement.tempo_bpm == 62: num_segs = random.choice([4, 5])
    if movement.tempo_bpm == 66: num_segs = random.choice([5, 6])
    if movement.tempo_bpm == 70: num_segs = random.choice([5, 6])
    if movement.tempo_bpm == 74: num_segs = random.choice([5, 6])
    if movement.tempo_bpm == 78: num_segs = random.choice([5, 6, 7])
    if movement.tempo_bpm == 82: num_segs = random.choice([6, 7])
    if movement.tempo_bpm == 86: num_segs = random.choice([6, 7, 8])
    if movement.tempo_bpm == 90: num_segs = random.choice([6, 7, 8])
    if movement.tempo_bpm == 94: num_segs = random.choice([6, 7, 8])
    if movement.tempo_bpm == 98: num_segs = random.choice([7, 8, 9])
    if movement.tempo_bpm == 102: num_segs = random.choice([7, 8, 9])
    
    movement.segment_order = random.choice(seg_order_opts[num_segs])    
    



def calculate_duration(movement):
    dur_of_sixteenths = 60.0/(movement.tempo_bpm*4)
    len_of_segments = movement.duration_of_segments
    num_of_segments = len(movement.segment_order)
    movement.duration = len_of_segments * num_of_segments
    movement.duration_seconds = dur_of_sixteenths * movement.duration

def set_guitar_rhythm_opts_per_harm(movement):
    opts = {}
    opts[8] = [[4,4], [8],[8]]
    opts[12] = [[8,4],[12],[12]]
    opts[16] = [[12,4], [16],[16]]
    opts[20] = [[12,8],[16,4],[20],[20]]
    opts[24] = [[12,12],[16,8],[16,4,4],[20,4],[24],[24]]
    opts[28] = [[16,12],[20,8],[20,4,4],[24,4],[28],[28]]
    opts[32] = [[12,4,12,4],[12,4,16],[4,28],[16,8,8],[16,16],[20,12],[24,4,4],[24,8],[28,4],[32],[32],[32]]
    opts[36] = [[20,8,8],[28,4,4],[28,8],[4,32],[32,4],[36]]
    opts[40] = [[24,8,4,4],[24,8,8],[24,16],[32,4,4],[4,36],[32,8],[36,4],[40],[40],[40]]
    opts[44] = [[28,8,4,4],[28,8,8],[36,4,4],[36,8],[40,4],[40],[40],[40]]
    opts[48] = [[32,8,4,4],[32,8,8],[40,8],[4,44],[40,4,4],[44,4],[48],[48],[48]]
    opts[52] = [[36,8,8],[44,4,4],[44,8],[48,4],[52],[52],[52]]
    opts[56] = [[40,8,8],[48,8],[56],[56],[56]]    
    opts[60] = [[44,8,8],[52,8],[60],[60],[60]]
    movement.guitar_rhythm_opts_per_harm = opts

    
def make_ensemble_roles(movement):
    movement.ensemble_func_dispatch = {
        #'chords_sustained_on_phrase_type': chords_sustained_on_phrase_type,
        'chords_sustained_on_phrase': chords_sustained_on_phrase,
        #'beg_and_end_chords_sustained_on_phrase_type': beg_and_end_chords_sustained_on_phrase_type,
        'beg_and_end_chords_sustained_on_phrase': beg_and_end_chords_sustained_on_phrase,        
        'resting': resting,
        #'drone': drone,
        'guitar_chords_on_phrase_type_unison':guitar_chords_on_phrase_type_unison,
        'guitar_chords_on_phrase_unison':guitar_chords_on_phrase_unison,
        'guitar_chords_on_phrase_type':guitar_chords_on_phrase_type,     
        'guitar_chords_on_phrase':guitar_chords_on_phrase,
        #'melody_on_phrase_type_unison':melody_on_phrase_type_unison,
        'melody_on_phrase_unison':melody_on_phrase_unison,
        'harmonize_melody':harmonize_melody,
        #'simple_melody_on_phrase_type_unison':simple_melody_on_phrase_type_unison,
        'simple_melody_on_phrase_unison':simple_melody_on_phrase_unison,
        'harmonize_simple_melody':harmonize_simple_melody,
##        'baritone_simple_melody_on_phrase_type_unison':baritone_simple_melody_on_phrase_type_unison,
##        'baritone_simple_melody_on_phrase_unison':baritone_simple_melody_on_phrase_unison,
##        'baritone_harmonize_simple_melody':baritone_harmonize_simple_melody
    }
    
        


def make_ensemble_order(movement):
    num_of_phrases = len(movement.phrases)
    opt_groups = [[1,1,1,2],[1,1,2,3],[2,3,4,4],[1,1,2,3,3]]
    movement.ensemble_order = []
    groups_of_phrases = divide_into_4(num_of_phrases)
    for num_phrases, opts in zip(groups_of_phrases, opt_groups):
        for x in range(num_phrases):
            ens = random.choice(opts)
            movement.ensemble_order.append(ens)
    for phrase, ens in zip(movement.phrases, movement.ensemble_order):
        phrase.ensemble_number = ens
        
        
def make_section_types(movement):
    print 'make_section_types'
    movement.segment_types = {}
    for type_name in movement.segment_type_names:
        make_section_type(type_name, movement)
    
def make_section_type(name, movement):
    print 'make_section_type'
    section_type = BaseEvent(start=0, duration=movement.duration_of_segments)
    section_type.name = name
    
    if name == 'I': section_type.ensemble_number = 1
    if name == 'II': section_type.ensemble_number = 2
    if name == 'III': section_type.ensemble_number = 3

    

    section_type.movement = movement
    section_type.num_of_segments = random.choice([1,2,2,4,4,4])
    section_type.segment_order = random.choice(movement.subsegment_order_options[section_type.num_of_segments])
    section_type.segment_type_names = list(set(section_type.segment_order))    
    movement.segment_types[name] = section_type 
    section_type.segment_types = {}
    section_type.schizoid_harmony = movement.schizoid_harmony
    
    root = random.choice(range(12))
    scale = random.choice([(0,2,4,7,9),(0,2,4,7,9),(0,2,5,6,7,9),(0,1,4,6,8,11),
                           (0,2,4,5,7,9,11),(0,2,4,5,7,9,11),(0,2,4,5,7,9,11),(0,2,4,5,7,9,11)
                           
##                           (0,1,2,4,5,7,9,11),
##                           (0,2,3,4,5,7,9,11),
##                           (0,2,4,5,6,7,9,11),
##                           (0,2,4,5,7,8,9,11),
##                           (0,2,4,5,7,9,10,11),
##                           
##                           (0,1,2,3,4,5,7,9,11),
##                           (0,1,2,4,5,6,7,9,11),
##                           (0,1,2,4,5,7,8,9,11),
##                           (0,1,2,4,5,7,9,10,11),
##                           (0,2,3,4,5,7,9,11),
##                           (0,2,3,4,5,6,7,9,11),                           
##                           (0,2,3,4,5,7,8,9,11),
##                           (0,2,3,4,5,7,9,10,11),
##                           (0,2,4,5,6,7,8,9,11),
##                           (0,2,4,5,6,7,9,10,11),
##                           (0,2,4,5,7,8,9,10,11),
##
##                           (0,1,2,3,4,5,6,7,9,11),
##                           (0,1,2,3,4,5,7,8,9,11),
##                           (0,1,2,3,4,5,7,9,10,11),
##                           
##                           (0,1,2,4,5,6,7,8,9,11),
##                           (0,1,2,4,5,6,7,9,10,11),
##                           (0,1,2,4,5,7,8,9,10,11),
##                           
##                           (0,2,3,4,5,6,7,8,9,11),
##                           (0,2,3,4,5,6,7,9,10,11),
##                           (0,2,4,5,6,7,8,9,10,11),
##                           
##                           (0,2,3,4,5,6,7,8,9,10,11),
##                           (0,1,2,4,5,6,7,8,9,10,11),
##                           (0,1,2,3,4,5,7,8,9,10,11),
##                           (0,1,2,3,4,5,6,7,9,10,11),
##                           (0,1,2,3,4,5,6,7,8,9,11),
##                           
##                           (0,1,2,3,4,5,6,7,8,9,10,11)
                           ])
    section_type.scale = [(pc + root) % 12 for pc in scale]
    
    make_harmony_options(section_type)

    section_type.ornamented = random.choice([True, False])  
    
    print section_type.name, 'ornamented', section_type.ornamented
    
    is_strumming = random.choice([True, False])
        
    section_type.register = {}
    section_type.strumming = {}
    
    for m in movement.musicians_names:
        section_type.register[m] = movement.musicians_by_name[m].instrument.conservative_register

        if is_strumming:
            section_type.strumming[m] = random.choice([True, True, False])
        else:
            section_type.strumming[m] = False
        make_keyboard_thickness(section_type)
    section_type.soprano_start_pitch = random.choice(range(6,13))

def make_phrase_types(movement):
    print 'make_phrase_types'
    for section_type_name in movement.segment_type_names:
        section_type = movement.segment_types[section_type_name]
        for phrase_type_name in section_type.segment_type_names:
            make_phrase_type(phrase_type_name, section_type)
    
    
def make_phrase_type(name, section_type):
    print 'make_phrase_type', section_type.name, name
    
    d = section_type.duration/section_type.num_of_segments
    phrase_type = BaseEvent(start=0, duration=d)    
    section_type.segment_types[name] = phrase_type    
    phrase_type.name = name
    
    phrase_type.ensemble_number = section_type.ensemble_number

    
    phrase_type.full_name = '{0} {1}'.format(section_type.name, phrase_type.name)
    phrase_type.section_type = section_type
    phrase_type.movement = section_type.movement
    phrase_type.harmony_options = section_type.harmony_options

    make_measures(phrase_type)
    make_harmonic_rhythm(phrase_type)
    
    phrase_type.scale = section_type.scale
    #make_harmonies(phrase_type)
    
    phrase_type.notes = {}
    phrase_type.register = {}
    phrase_type.rhythm = {}
    for m in phrase_type.movement.musicians_names:
        phrase_type.register[m] = section_type.register[m]
        phrase_type.notes[m] = []
        phrase_type.movement.notes[m] = []

    
#    phrase_type.chords_sustained_on_phrase_type = {}
#    for m in section_type.movement.musicians_names:
#        phrase_type.chords_sustained_on_phrase_type[m] = \
#                   chords_sustained(phrase_type, m)

##    phrase_type.beg_and_end_chords_sustained_on_phrase_type = {}
##    for m in ['Quentin', 'Phil', 'Will']:
##        phrase_type.beg_and_end_chords_sustained_on_phrase_type[m] = \
##                   beg_and_end_chords_sustained(phrase_type, m)


##    guitar_chords(phrase_type, 'Matt')
##    guitar_chords(phrase_type, 'Ian')
#    phrase_type.melody_for_phrase_type_unison = melody(phrase_type)
    
    
    
#    phrase_type.simple_melody_for_phrase_type_unison = simple_melody(phrase_type)
    #phrase_type.baritone_simple_melody_for_phrase_type_unison = baritone_simple_melody(phrase_type)
    
        
    
        
        
        
        
        
        
    
def make_phrases(movement):
    movement.sections = []
    movement.phrases = []
    seq_num = 1
    s1 = movement.start
    s2 = movement.start

##    prev_pitches = [random.choice(range(6,11))]
##    prev_pitches.append(prev_pitches[0] - 1)    
    
    prev_harms = []

    for section_type_name in movement.segment_order:
        section = movement.segment_types[section_type_name]
        new_section = deepcopy_Event(section, new_start=s1)
        movement.sections.append(new_section)
        s1 += new_section.duration        
        
        for phrase_type_name in new_section.segment_order:
            phrase = new_section.segment_types[phrase_type_name]
            new_phrase = deepcopy_Event(phrase, new_start=s2)
            new_phrase.full_name = '{0:<4}{1:<4}{2}'.format('{0}:'.format(seq_num), \
                                                       section_type_name, \
                                                       phrase_type_name)
            
         
            make_harmonies(new_phrase, prev_harms)
            

            new_phrase.melody_for_phrase_unison = melody(new_phrase)#, prev_pitches)
            
##            get_lyrics(new_phrase.melody_for_phrase_type_unison)
##            get_lyrics(new_phrase.melody_for_phrase_unison)
            
            new_phrase.simple_melody_for_phrase_unison = simple_melody(new_phrase)
            #new_phrase.baritone_simple_melody_for_phrase_unison = baritone_simple_melody(new_phrase)
            
            
            movement.phrases.append(new_phrase)
            movement.measures.extend(new_phrase.measures)
            s2 += new_phrase.duration
            seq_num += 1

def get_lyrics(notes):
    # get rhythm
    # make lyrics meter
    # get words
    durs = [n.duration for n in notes if n.pitches]
    len_durs = len(durs)
    
    if len_durs == 1:
        for n in notes:
            n.lyric = 'ah'
    elif len_durs == 2:
        stresses = random.choice(['10', '01'])
        rawlinetypes = [('A', stresses[0], stresses[1])]
        rawlines = [(stresses,'A')]
        add_lyrics(rawlinetypes, rawlines, notes)
        
    elif len_durs == 3:    
        rawlinetypes = [('A', '10', '1')]
        rawlines = [('101','A')]
        add_lyrics(rawlinetypes, rawlines, notes)        
    elif len_durs == 4:    
        rawlinetypes = [('A', '010', '1')]
        rawlines = [('0101','A')]
        add_lyrics(rawlinetypes, rawlines, notes)  
    elif len_durs == 5:    
        rawlinetypes = [('A', '0010', '1')]
        rawlines = [('00101','A')]
        add_lyrics(rawlinetypes, rawlines, notes)     
    elif len_durs == 6:    
        rawlinetypes = [('A', '10', '1')]
        rawlines = [('101','A'),('101','A')]
        add_lyrics(rawlinetypes, rawlines, notes)      
    elif len_durs == 7:    
        rawlinetypes = [('A', '101010', '1')]
        rawlines = [('1010101','A')]
        add_lyrics(rawlinetypes, rawlines, notes)   
    elif len_durs == 8:    
        rawlinetypes = [('A', '010', '1')]
        rawlines = [('0101','A'),('0101','A')]
        add_lyrics(rawlinetypes, rawlines, notes)     
    elif len_durs == 9:    
        rawlinetypes = [('A', '00100100', '1')]
        rawlines = [('001001001','A')]
        add_lyrics(rawlinetypes, rawlines, notes)   
    elif len_durs == 10:    
        rawlinetypes = [('A', '0100', '1')]
        rawlines = [('01001','A'), ('01001','A')]
        add_lyrics(rawlinetypes, rawlines, notes)   
    elif len_durs == 11:    
        rawlinetypes = [('A', '0100100100', '1')]
        rawlines = [('01001001001','A')]
        add_lyrics(rawlinetypes, rawlines, notes)  
    elif len_durs == 12:    
        rawlinetypes = [('A', '10', '1'),('B', '10', '1')]
        rawlines = [('101','A'), ('101','B'),('101','A'),('101','B')]
        add_lyrics(rawlinetypes, rawlines, notes)  
    elif len_durs == 13:    
        rawlinetypes = [('A', '00100100100', '10')]
        rawlines = [('0010010010010','A')]
        add_lyrics(rawlinetypes, rawlines, notes) 
    elif len_durs == 14:    
        rawlinetypes = [('A', '100100', '1')]
        rawlines = [('1001001','A'), ('1001001','A')]
        add_lyrics(rawlinetypes, rawlines, notes)     
    elif len_durs == 15:    
        rawlinetypes = [('A', '0100', '1')]
        rawlines = [('01001','A'),('01001','A'),('01001','A')]
        add_lyrics(rawlinetypes, rawlines, notes)
    else:
        
        quarter = len_durs/4
        big_quarter = quarter + 1
        if len_durs % 4 == 0:
            line_order_opts = [
                'AAAA',
                'ABAB','ABAB','ABAB','ABAB','ABAB','ABAB','ABAB','ABAB','ABAB','ABAB',
                'ABBA', 
                'ABBB', 
                'AABA','ABAA', 
                'AABB','AABB','AABB','AABB','AABB','AABB','AABB','AABB','AABB','AABB',    
            ]
            A_pre, A_mid, A_end = get_line_stresses(quarter)
            B_pre, B_mid, B_end = get_line_stresses(quarter)

        elif len_durs % 4 == 1:
            if random.choice([True, False]):
                A_size = big_quarter
                B_size = quarter
                line_order_opts = ['ABBB']                
            else:
                A_size = quarter
                B_size = big_quarter
                line_order_opts = ['AAAB', 'AABA', 'ABAA']
            A_pre, A_mid, A_end = get_line_stresses(A_size)
            B_pre, B_mid, B_end = get_line_stresses(B_size) 
        elif len_durs % 4 == 2:  
            line_order_opts = [
                'ABAB','ABAB','ABAB','ABAB','ABAB','ABAB','ABAB','ABAB','ABAB','ABAB',
                'ABBA', 
                'AABB','AABB','AABB','AABB','AABB','AABB','AABB','AABB','AABB','AABB',    
            ]             
            A_size = quarter
            B_size = quarter
            A_pre, A_mid, A_end = get_line_stresses(A_size)
            B_pre, B_mid, B_end = get_line_stresses(B_size)            
        elif len_durs % 4 == 3:
            if random.choice([True, False]):
                A_size = quarter
                B_size = big_quarter
                line_order_opts = ['ABBB']                
            else:
                A_size = big_quarter
                B_size = quarter
                line_order_opts = ['AAAB', 'AABA', 'ABAA']

            A_pre, A_mid, A_end = get_line_stresses(A_size)
            B_pre, B_mid, B_end = get_line_stresses(B_size) 
            
        line_order = random.choice(line_order_opts)
        
        linetypes = {}
        print A_pre, A_mid, A_end
        linetypes['A'] = ('A', A_pre + A_mid, A_end)
        linetypes['B'] = ('B', B_pre + B_mid, B_end)
        rawlinetypes = [linetypes['A'], linetypes['B']]

        lines = {}
        lines['A'] = (A_pre + A_mid + A_end, 'A')
        lines['B'] = (B_pre + B_mid + B_end, 'B')
        rawlines = []
        for letter in line_order:
            rawlines.append(lines[letter])
            
##        rawlines = [
##            ('100100100100','A'),
##            ('1010101', 'B'),
##            ('100100100100','A'),
##            ('1010101', 'B')]

        print lines
        print linetypes
        
        add_lyrics(rawlinetypes, rawlines, notes)
        
def get_line_stresses(num_notes):
    # 4 and up notes
    # possible prefixes: None, '0', '00'
    # repeating mid: '10' or '100'
    # possible end: '1', '10', '100'
    # 
    # possibilities for 4: (None, 100, 1), (None, 10, 10), (0, 10, 1)
    # 5: (None, 10, 100), (None, 100, 10), (None, 1010, 1), (0, 10, 10), (0, 100, 1) (00, 10, 1)
    # 6: (None, 10),
    # 14: 

    opts = []
    if num_notes - 1 < 5:
        sub = num_notes - 1
    else:
        sub = 5
    for len_mid in range(num_notes - sub, num_notes):
        remaining = num_notes - len_mid
        
        pres_ends = get_pres_ends(remaining)
        
        mid_opts = []
        if len_mid % 2 == 0:
            mid_opt = '10' * (len_mid / 2)
            mid_opts.append(mid_opt)
        if len_mid % 3 == 0:
            mid_opt = '100' * (len_mid / 3)
            mid_opts.append(mid_opt)

        for mid_o in mid_opts:
            for p_e in pres_ends:
                opt = (p_e[0], mid_o, p_e[1])
                opts.append(opt)
    
    pre, mid, end = random.choice(opts)
    
    return pre, mid, end

def get_pres_ends(d):
    if d == 1: result = [('','1')]
    if d == 2: result = [('','10'), ('0','1')]
    if d == 3: result = [('','100'), ('0','10'), ('00','1')]
    if d == 4: result = [('0','100'), ('00','10')]    
    if d == 5: result = [('00','100')]
    return result
    
        
def add_lyrics(rawlinetypes, rawlines, notes):        
    structure = get_poem_structure(rawlinetypes, rawlines)
    poem = make_poem(structure)
    syllables = []
    for line in poem.lines:
        for syl in line.syllables:
            syllables.append(syl)
    
    notes = [n for n in notes if n.pitches]
    for n, s in zip(notes, syllables):
        n.lyric = s
        
            
            
def make_parts_on_phrases(movement):
    for phrase in movement.phrases:
        ens_num = phrase.ensemble_number
        ensemble = movement.ensembles[ens_num]
        for role in reversed(sorted(ensemble)):
            f = movement.ensemble_func_dispatch[role]
            for m in ensemble[role]:
                f(phrase, m)

def phrase_notes_to_musicians(movement):
    for m in movement.musicians_names:
        for phrase in movement.phrases:
            movement.musicians_by_name[m].music.extend(phrase.notes[m])    
    
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

def make_harmony_options(segment):
    segment.chordtypes = []
    if segment.name == 'I' or segment.name == 'II':
        chordtypes = preferred_chordtypes[3] + \
                   preferred_chordtypes[3] + preferred_chordtypes[3] + \
                   preferred_chordtypes[2]
    if segment.name == 'III':
        if random.choice([True,False]) == True:
            chordtypes = preferred_chordtypes[3] + \
                       preferred_chordtypes[2] + preferred_chordtypes[2]
        else:
            chordtypes = preferred_chordtypes[4] + \
                       preferred_chordtypes[3]           
    opts = chordtypes_on_roots(chordtypes)
    #segment.harmony_options = containing(opts, [segment.movement.drone_pc])

##    num_pcs_omit = random.choice([0,1,2])
##    chrom = range(12)
##    for n in range(num_pcs_omit):
##        killl = random.choice(chrom)
##        chrom.remove(killl)

    
    all_scales = chordtypes_on_roots([(0,2,4,5,7,9,11)])
    num_scales = random.choice([1,2,3,4])
    chosen_scales = random.sample(all_scales, num_scales)
    
    chrom = []
    for sc in chosen_scales:
        for pi in sc:
            if pi not in chrom:
                chrom.append(pi)
    
    segment.harmony_options = chords_in_scale(opts, chrom)

    #all_scales = chordtypes_on_roots([(0,2,4,5,7,9,11),(0,2,4,5,7,9,11),(0,2,4,5,7,9,11),(0,2,4,7,9),(0,2,4,7,9),(0,1,4,6,8,11)])
    #segment.scale_options = containing(all_scales, [segment.movement.drone_pc])
    
def make_harmonies(segment, prev_harms):
    segment.harmonies = []
    previous_chord = random.choice(segment.harmony_options)
    prev_sharps_or_flats = 'sharps'
    s = segment.start

    print segment.section_type.name
    
    for d in segment.harmonic_rhythm:
        harmony = BaseEvent(start=s, duration=d)
        s += d
        harmony.pitches = choose_harmony(prev_harms, segment.harmony_options)

            
        #print harmony.pitches
        root_change, harmony.chordtype = get_chordtype(harmony.pitches)
        harmony.root = (harmony.pitches[0] + root_change) % 12
        #print harmony.root, harmony.chordtype

##        scale_type_options = [
##            (0,2,4,7,9),(0,2,4,7,9),
##            (0,2,4,5,7,9),
##            (0,2,4,5,7,9,11),(0,2,4,5,7,9,11),(0,2,4,5,7,9,11)
##        ]


        scale_type_options = chords_scales[harmony.chordtype]
        
        
        scale_options = get_scales_containing_chord(harmony.pitches, scale_type_options)
        harmony.scale = random.choice(scale_options)
        
        diatonic_scale_types = [
            (0,2,4,5,7,9,11),(0,2,4,5,7,9,11),(0,2,4,5,7,9,11),(0,2,4,5,7,9,11),
            (0,1,4,6,9,11), # marwa
            (0,2,5,6,7,9) # blues
        ]
        harmony.diatonic = random.choice(get_scales_containing_chord(harmony.scale, diatonic_scale_types))

        
        print '{0:<20}{1}'.format(harmony.pitches, harmony.scale)
        
        harmony.sharps_or_flats = chordSharpsOrFlats(list(harmony.pitches), prev_sharps_or_flats)        
        segment.harmonies.append(harmony)
        segment.movement.harmonies_tracker.append(harmony)
        
        segment.movement.harmonies.append(harmony)        
        
        previous_chord = harmony.pitches     

def choose_harmony(prev_harms, harmony_options):
    if len(prev_harms) > 9:
        to_delete = random.choice(prev_harms)
        prev_harms.remove(to_delete)
    chosen_harmony = random.choice(harmony_options) #get_chord(segment, previous_chord)
    if chosen_harmony not in prev_harms:
        prev_harms.append(chosen_harmony)
        return chosen_harmony
    else:
        return choose_harmony(prev_harms, harmony_options)
        
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

def harmonize_simple_melody(segment, m):      
    ensemble = segment.movement.ensembles[segment.ensemble_number]
    musicians = ensemble['simple_melody_on_phrase_unison'] #+ ensemble['simple_melody_on_phrase_type_unison']
    melody_musician = random.choice(musicians)    
    first_note = segment.notes[melody_musician][0].pitches
    first_note = first_note[0]
    previous_note = random.choice([first_note + 7, first_note - 7])
    
    
    
    prevs = [previous_note, previous_note]
    for n in segment.notes[melody_musician]:
        new_n = deepcopy_Event(n)
        segment.notes[m].append(new_n)
        if new_n.pitches:
            pitch_to_harmonize = n.pitches
            pitch_to_harmonize = pitch_to_harmonize[0]
            register = segment.movement.musicians_by_name[m].instrument.conservative_register
            harmony = get_at_microbeat(n.start, segment.harmonies)
            harmony = harmony[0]
            pitch = get_next_simple_harmony_pitch(pitch_to_harmonize, prevs, harmony.pitches, harmony.scale, register)
            prevs.append(pitch)
            new_n.pitches = [pitch]            
            
            
def get_next_simple_harmony_pitch(pitch_to_harmonize, prevs, harmony, scale, register):

    preferred_distance_from_previous = range(prevs[-1] - 5, prevs[-1] + 6)
    acceptable_distance_from_previous = range(prevs[-1] - 8, prevs[-1] + 9)
    acceptable_distance_from_two_previous = range(prevs[-2] - 7, prevs[-2] + 8)
    acceptable_intervals = [0,3,4,5,7,8,9]

    in_scale_preferred = []
    in_scale = []
    in_harmony_preferred = []
    in_harmony = []
    pretty_bad = []
    last_resort = []
    beyond_last_resort = []
    
    for p in register:
        if ((pitch_to_harmonize - p) % 12) in acceptable_intervals:
            beyond_last_resort.append(p)
            if p in acceptable_distance_from_previous:
                last_resort.append(p)
                if p in acceptable_distance_from_two_previous:
                    pretty_bad.append(p)
                    if p % 12 in scale:
                        in_scale.append(p)
                        if p in preferred_distance_from_previous:
                            in_scale_preferred.append(p)

                    if p % 12 in harmony:
                        in_harmony.append(p)
                        if p in preferred_distance_from_previous:
                            in_harmony_preferred.append(p)
    
    all_weights = []
    for a in range(len(in_harmony_preferred)):
        all_weights.append(1600)
    for a in range(len(in_harmony)):
        all_weights.append(800)
    for a in range(len(in_scale_preferred)):
        all_weights.append(100)
    for a in range(len(in_scale)):
        all_weights.append(50)
    for a in range(len(pretty_bad)):
        all_weights.append(10)
    for a in range(len(last_resort)):
        all_weights.append(2)
    for a in range(len(beyond_last_resort)):
        all_weights.append(1)
        
    all_opts = in_harmony_preferred + in_harmony + in_scale_preferred + in_scale + pretty_bad + last_resort + beyond_last_resort
    chosen = weighted_choice(all_opts, all_weights)  
    return chosen
##    opts = in_harmony_preferred + in_harmony_preferred + \
##         in_harmony_preferred + in_scale_preferred + \
##         in_scale_preferred + in_scale_preferred + \
##         in_harmony + in_harmony + in_scale
##    if not opts:
##        opts += pretty_bad
##    if not opts:
##        opts += last_resort
##    if not opts:
##        opts += beyond_last_resort
##    if not opts:
##        opts += register
##    return random.choice(opts)


def simple_melody_on_phrase_type_unison(segment, m):
    segment.notes[m] = []
    s = segment.start
    for n in segment.simple_melody_for_phrase_type_unison:
        new_n = deepcopy_Event(n, new_start=s)
        s += new_n.duration
        segment.notes[m].append(new_n)
            
def simple_melody_on_phrase_unison(segment, m):
    segment.notes[m] = []
    s = segment.start
    for n in segment.simple_melody_for_phrase_unison:
        new_n = deepcopy_Event(n, new_start=s)
        s += new_n.duration
        segment.notes[m].append(new_n)
def simple_melody(segment):

    num_half_bars = segment.duration/8
    if num_half_bars == 4:
        num_beg_half_bars = 1
        num_end_half_bars = 1
    elif num_half_bars == 8:
        num_beg_half_bars = random.choice([1,1,2,2,2])
        num_end_half_bars = random.choice([1,1,1,2])
    elif num_half_bars == 16:
        num_beg_half_bars = random.choice([1,2,2,3,3,3])
        num_end_half_bars = random.choice([1,2])
    
    if num_beg_half_bars:
        beg_notes = get_simple_melody_chunk(segment, num_beg_half_bars, segment.start)
        rest_start = beg_notes[-1].next_event_start
    else:
        beg_notes = []
        rest_start = segment.start
    
    end_start = segment.start + segment.duration - (num_end_half_bars*8)
    end_notes = get_simple_melody_chunk(segment, num_end_half_bars, end_start)
    
    rests_dur = end_start - rest_start
    rests_half_notes = rests_dur/8
    rests = []
    s = rest_start
    for counter in range(rests_half_notes):
        r = Event(start=s, duration=8)
        s += r.duration
        r.pitches = []
        rests.append(r)
        harmony = get_at_microbeat(r.start, segment.harmonies)
        harmony = harmony[0]
        r.sharps_or_flats = harmony.sharps_or_flats

    notes = beg_notes + rests + end_notes

    return notes

def get_simple_melody_chunk(segment, num_beg_half_bars, start):
    notes = []

    # match with lyrics somehow
    register = range(0,18)
    prev_pitches = [random.choice(range(6,10))]
    prev_pitches.append(prev_pitches[0] - 1)
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    s = start
    for half_bar in range(num_beg_half_bars):
        start_harmony = get_at_microbeat(s, segment.harmonies)
        start_harmony = start_harmony[0]
        upbeat_harmony = get_at_microbeat(s + 4, segment.harmonies)
        upbeat_harmony = upbeat_harmony[0]
        if start_harmony.pitches == upbeat_harmony.pitches:
            durs = get_simple_melody_rhythm_chunk(8)
            for d in durs:
                e = Event(start=s, duration=d)
                s += e.duration
                notes.append(e)    
                if e.start == segment.start:
                    e.rehearsal = True
                    e.rehearsal_type = 'plain'
                    e.rehearsal_text = rehearsal_text
                e.sharps_or_flats = start_harmony.sharps_or_flats
                
                pitch = get_next_simple_melody_pitch(prev_pitches, 
                                                 start_harmony.pitches, 
                                                 start_harmony.scale,
                                                 register)
                e.pitches = [pitch]
                prev_pitches.append(pitch)
        else:
            durs = get_simple_melody_rhythm_chunk(4)
            for d in durs:
                e = Event(start=s, duration=d)
                s += e.duration
                notes.append(e)    
                if e.start == segment.start:
                    e.rehearsal = True
                    e.rehearsal_type = 'plain'
                    e.rehearsal_text = rehearsal_text
                e.sharps_or_flats = start_harmony.sharps_or_flats
                pitch = get_next_simple_melody_pitch(prev_pitches, 
                                                 start_harmony.pitches, 
                                                 start_harmony.scale,
                                                 register)
                e.pitches = [pitch]            
                prev_pitches.append(pitch)
                
            durs = get_simple_melody_rhythm_chunk(4)
            for d in durs:
                e = Event(start=s, duration=d)
                s += e.duration
                notes.append(e)    
                if e.start == segment.start:
                    e.rehearsal = True
                    e.rehearsal_type = 'plain'
                    e.rehearsal_text = rehearsal_text
                e.sharps_or_flats = upbeat_harmony.sharps_or_flats
                pitch = get_next_simple_melody_pitch(prev_pitches, 
                                                 start_harmony.pitches, 
                                                 start_harmony.scale,
                                                 register)
                e.pitches = [pitch]       
                prev_pitches.append(pitch)
    return notes    

def get_next_simple_melody_pitch(prevs, harmony, scale, register):
    scale_pitches = [p for p in register if p % 12 in scale]
    chord_pitches = [p for p in register if p % 12 in harmony]
    preferred = []
    secondary = []
    preferred1 = []
    secondary1 = []    
    if prevs[-1] in scale_pitches: 
        secondary.append(prevs[-1])
    if prevs[-2] in scale_pitches: preferred.append(prevs[-2])
    if prevs[-1] + 1 in scale_pitches: preferred.append(prevs[-1] + 1)
    if prevs[-1] + 2 in scale_pitches: preferred.append(prevs[-1] + 2)
    if prevs[-1] + 3 in scale_pitches: preferred.append(prevs[-1] + 3)
    if prevs[-1] + 4 in scale_pitches: secondary.append(prevs[-1] + 4)
    if prevs[-1] + 5 in scale_pitches: secondary.append(prevs[-1] + 5)
    if prevs[-1] - 1 in scale_pitches: preferred.append(prevs[-1] - 1)
    if prevs[-1] - 2 in scale_pitches: preferred.append(prevs[-1] - 2)
    if prevs[-1] - 3 in scale_pitches: preferred.append(prevs[-1] - 3)
    if prevs[-1] - 4 in scale_pitches: secondary.append(prevs[-1] - 4)
    if prevs[-1] - 5 in scale_pitches: secondary.append(prevs[-1] - 5)
    if prevs[-1] in chord_pitches: 
        if random.choice([True, True, True, True, False]):
            secondary1.append(prevs[-1])
        else:
            preferred1.append(prevs[-1])
    if prevs[-1] + 1 in chord_pitches: preferred1.append(prevs[-1] + 1)
    if prevs[-1] + 2 in chord_pitches: preferred1.append(prevs[-1] + 2)
    if prevs[-1] + 3 in chord_pitches: preferred1.append(prevs[-1] + 3)
    if prevs[-1] + 4 in chord_pitches: secondary1.append(prevs[-1] + 4)
    if prevs[-1] + 5 in chord_pitches: secondary1.append(prevs[-1] + 5)
    if prevs[-1] - 1 in chord_pitches: preferred1.append(prevs[-1] - 1)
    if prevs[-1] - 2 in chord_pitches: preferred1.append(prevs[-1] - 2)
    if prevs[-1] - 3 in chord_pitches: preferred1.append(prevs[-1] - 3)
    if prevs[-1] - 4 in chord_pitches: secondary1.append(prevs[-1] - 4)
    if prevs[-1] - 5 in chord_pitches: secondary1.append(prevs[-1] - 5)
    
##    if preferred:
##        pitch = random.choice(preferred)
##    elif secondary:
##        pitch = random.choice(secondary)        
##    else:
##        pitch = random.choice(chord_pitches)        

        
    all_weights = []
    for a in range(len(preferred1)):
        all_weights.append(16)
    for a in range(len(secondary1)):
        all_weights.append(10)
       
    for a in range(len(preferred)):
        all_weights.append(8)
    for a in range(len(secondary)):
        all_weights.append(5)

        
    all_opts = preferred1 + secondary1 + preferred + secondary
    pitch = weighted_choice(all_opts, all_weights)        
        
    
    return pitch

def get_simple_melody_rhythm_chunk(duration):
    opts = {
        4:[[4]],
        8:[[8],[8],[8],[8],[4,4]]
    }
    return random.choice(opts[duration])

#---------------------------------------

#---------------------------------------
def harmonize_melody(segment, m):
    ensemble = segment.movement.ensembles[segment.ensemble_number]
    musicians = ensemble['melody_on_phrase_unison'] #+ ensemble['melody_on_phrase_type_unison']
    melody_musician = random.choice(musicians)

    for n in segment.notes[melody_musician]:
        if n.pitches:
            first_note = n.pitches[0]
            break

    previous_note = random.choice([first_note + 7, first_note - 7])
    
    prevs = [previous_note, previous_note]
    for n in segment.notes[melody_musician]:
        new_n = deepcopy_Event(n)
        segment.notes[m].append(new_n)
        if new_n.pitches:
            pitch_to_harmonize = n.pitches
            pitch_to_harmonize = pitch_to_harmonize[0]
            register = segment.movement.musicians_by_name[m].instrument.conservative_register
            harmony = get_at_microbeat(n.start, segment.harmonies)
            harmony = harmony[0]
            pitch = get_next_harmony_pitch(pitch_to_harmonize, prevs, harmony.pitches, harmony.scale, register)
            prevs.append(pitch)
            new_n.pitches = [pitch]

def get_next_harmony_pitch(pitch_to_harmonize, prevs, harmony, scale, register):

    preferred_distance_from_previous = range(prevs[-1] - 5, prevs[-1] + 6)
    acceptable_distance_from_previous = range(prevs[-1] - 8, prevs[-1] + 9)
    acceptable_distance_from_two_previous = range(prevs[-2] - 7, prevs[-2] + 8)
    acceptable_intervals = [3,4,5,7,8,9]

    in_scale_preferred = []
    in_scale = []
    in_harmony_preferred = []
    in_harmony = []
    pretty_bad = []
    last_resort = []
    beyond_last_resort = []
    
    for p in register:
        if ((pitch_to_harmonize - p) % 12) in acceptable_intervals:
            beyond_last_resort.append(p)
            if p in acceptable_distance_from_previous:
                last_resort.append(p)                
                if p in acceptable_distance_from_two_previous:
                    pretty_bad.append(p)
                    if p % 12 in scale:
                        in_scale.append(p)
                        if p in preferred_distance_from_previous:
                            in_scale_preferred.append(p)

                    if p % 12 in harmony:
                        in_harmony.append(p)
                        if p in preferred_distance_from_previous:
                            in_harmony_preferred.append(p)
                            

    all_weights = []
    for a in range(len(in_harmony_preferred)):
        all_weights.append(1600)
    for a in range(len(in_harmony)):
        all_weights.append(800)
    for a in range(len(in_scale_preferred)):
        all_weights.append(300)
    for a in range(len(in_scale)):
        all_weights.append(100)
    for a in range(len(pretty_bad)):
        all_weights.append(10)
    for a in range(len(last_resort)):
        all_weights.append(2)
    for a in range(len(beyond_last_resort)):
        all_weights.append(1)
        
    all_opts = in_harmony_preferred + in_harmony + in_scale_preferred + in_scale + pretty_bad + last_resort + beyond_last_resort
    chosen = weighted_choice(all_opts, all_weights)     

    
##    opts = in_harmony_preferred + in_harmony_preferred + \
##         in_harmony_preferred + in_scale_preferred + \
##         in_scale_preferred + in_scale_preferred + \
##         in_harmony + in_harmony + in_scale
##    if not opts:
##        opts += pretty_bad
##    if not opts:
##        opts += last_resort
##    if not opts:
##        opts += beyond_last_resort
##    if not opts:
##        opts += register
##    chosen = random.choice(opts)
    
    
    
    return chosen


def melody_on_phrase_type_unison(segment, m):
    segment.notes[m] = []
    s = segment.start
    for n in segment.melody_for_phrase_type_unison:
        new_n = deepcopy_Event(n, new_start=s)
        s += new_n.duration
        segment.notes[m].append(new_n)
            
def melody_on_phrase_unison(segment, m):
    segment.notes[m] = []
    s = segment.start
    for n in segment.melody_for_phrase_unison:
        new_n = deepcopy_Event(n, new_start=s)
        s += new_n.duration
        segment.notes[m].append(new_n)

def get_next_melody_pitch(prevs, harmony, scale, register):
    scale_pitches = [p for p in register if p % 12 in scale]
    chord_pitches = [p for p in register if p % 12 in harmony]
    preferred = []
    secondary = []
    tertiary = []
    preferred1 = []
    secondary1 = []
    tertiary1 = []    
    if prevs[-1] in scale_pitches: 
        secondary.append(prevs[-1])
    if prevs[-2] in scale_pitches: preferred.append(prevs[-2])
    if prevs[-1] + 1 in scale_pitches: preferred.append(prevs[-1] + 1)
    if prevs[-1] + 2 in scale_pitches: preferred.append(prevs[-1] + 2)
    if prevs[-1] + 3 in scale_pitches: tertiary.append(prevs[-1] + 3)
    if prevs[-1] + 4 in scale_pitches: tertiary.append(prevs[-1] + 4)
    if prevs[-1] + 5 in scale_pitches: tertiary.append(prevs[-1] + 5)
    if prevs[-1] - 1 in scale_pitches: preferred.append(prevs[-1] - 1)
    if prevs[-1] - 2 in scale_pitches: preferred.append(prevs[-1] - 2)
    if prevs[-1] - 3 in scale_pitches: tertiary.append(prevs[-1] - 3)
    if prevs[-1] - 4 in scale_pitches: tertiary.append(prevs[-1] - 4)
    if prevs[-1] - 5 in scale_pitches: tertiary.append(prevs[-1] - 5)
    if prevs[-1] in chord_pitches: 
        secondary1.append(prevs[-1])
    if prevs[-1] + 1 in chord_pitches: preferred1.append(prevs[-1] + 1)
    if prevs[-1] + 2 in chord_pitches: preferred1.append(prevs[-1] + 2)
    if prevs[-1] + 3 in chord_pitches: tertiary1.append(prevs[-1] + 3)
    if prevs[-1] + 4 in chord_pitches: tertiary1.append(prevs[-1] + 4)
    if prevs[-1] + 5 in chord_pitches: tertiary1.append(prevs[-1] + 5)
    if prevs[-1] - 1 in chord_pitches: preferred1.append(prevs[-1] - 1)
    if prevs[-1] - 2 in chord_pitches: preferred1.append(prevs[-1] - 2)
    if prevs[-1] - 3 in chord_pitches: tertiary1.append(prevs[-1] - 3)
    if prevs[-1] - 4 in chord_pitches: tertiary1.append(prevs[-1] - 4)
    if prevs[-1] - 5 in chord_pitches: tertiary1.append(prevs[-1] - 5)
    
    
    all_weights = []
    for a in range(len(preferred1)):
        all_weights.append(16)
    for a in range(len(secondary1)):
        all_weights.append(10)
    for a in range(len(tertiary1)):
        all_weights.append(6)
       
    for a in range(len(preferred)):
        all_weights.append(8)
    for a in range(len(secondary)):
        all_weights.append(5)
    for a in range(len(tertiary)):
        all_weights.append(3)
##    for a in range(len(chord_pitches)):
##        all_weights.append(1)
        
        
    all_opts = preferred1 + secondary1 + tertiary1 + preferred + secondary + tertiary
##    all_opts = preferred + secondary + tertiary
    pitch = weighted_choice(all_opts, all_weights)
    
##    if preferred:
##        pitch = random.choice(preferred)
##    elif secondary:
##        pitch = random.choice(secondary)        
##    elif tertiary:
##        pitch = random.choice(tertiary)  
##    else:
##        pitch = random.choice(chord_pitches)
    
    
    return pitch


def melody(segment):#, prev_pitches):
    register = range(0,18)
    
    prev_pitches = [random.choice(range(6,11))]
    prev_pitches.append(prev_pitches[0] - 1)
    notes = []
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    s = segment.start
    for measure in segment.measures:
        rhythm = get_melody_measure_rhythm(measure, segment)
        for r in rhythm:
            n = Event(start=s, duration=r[1])
            s += n.duration
            notes.append(n)
            if n.start == segment.start:
                n.rehearsal = True
                n.rehearsal_type = 'plain'
                n.rehearsal_text = rehearsal_text
            
            if not r[0]:
                n.pitches = []
            else:
                h = get_at_microbeat(n.start, segment.harmonies)
                h = h[0]
                n.sharps_or_flats = h.sharps_or_flats
                
                pitch = get_next_melody_pitch(prev_pitches, 
                                            h.pitches, 
                                            h.scale,
                                            register)
                n.pitches = [pitch]
                prev_pitches.append(pitch)            

    notes[0].slur = 'start'  
    notes[-1].slur = 'stop'
    return notes

def get_melody_measure_rhythm(measure, segment):
    s1 = measure.start
    s2 = s1 + 4
    s3 = s2 + 4
    s4 = s3 + 4
    h1 = get_at_microbeat(s1, segment.harmonies)
    h1 = h1[0].pitches
    h2 = get_at_microbeat(s2, segment.harmonies)
    h2 = h2[0].pitches        
    h3 = get_at_microbeat(s3, segment.harmonies)
    h3 = h3[0].pitches
    h4 = get_at_microbeat(s4, segment.harmonies)
    h4 = h4[0].pitches
    
    a = h1 == h2
    b = h1 == h3
    c = h1 == h4
    d = h2 == h3
    e = h2 == h4
    f = h3 == h4
    
    if a and b and c and d and e and f:
        durs = [16]
    elif a and b and d and not c and not e and not f:
        durs = [12,4]
    elif a and f and not b and not c and not d and not e:
        durs = [8,8]
    elif d and e and f and not a and not b and not c:
        durs = [4,12]
    elif d and not a and not b and not c and not e and not f:
        durs = [4,8,4]
    
    rhythm = []
    for dur in durs:
        rs = get_melody_rhythm_durs(dur)
        for r in rs:
            if type(r) == type([]):
                rhythm.extend(r)
            else:
                rhythm.append(r)
    return rhythm


def get_melody_rhythm_durs(duration):
    opts = {}
    opts[4] = [ [(False,4)], [(True,4)], [(True,4)], [(True,2),(True,2)], [(False,4)], [(True,4)] ]

    opts[8] = [ [(True,8)], [(True,8)], [(True,8)], [(True,8)], [(False,8)], [(False,8)], 
                [(True,4),(True,4)], [(True,4),(True,4)], 
                [(True,4),(False,4)],                
                [(True,4),(True,2),(True,2)],
                [(True,4),(True,2),(True,2)], [(True,2),(True,2),(True,2),(True,2)], [(True,4),(False,4)],
                [(True,2),(True,2),(True,2),(True,2)],
                [(True,6),(True,2)],[(True,6),(True,2)],[(True,6),(True,2)],[(True,6),(True,2)],
                [(True,6),(True,2)],[(True,6),(True,2)],[(True,6),(True,2)],[(True,6),(True,2)],
                [(True,6),(True,2)],[(True,6),(True,2)],[(True,6),(True,2)],[(True,6),(True,2)]
    ]
    
    opts[12] = [ 
        [(True,12)], [(False,12)], 
        [(True,8),(True,4)], [(True,8),(False,4)], [(False,8),(True,4)],
        [(True,8),(True,2),(True,2)], [(False,8),(True,2),(True,2)], 
        [(True,4),(True,8)], [(True,4),(False,8)], [(False,4),(True,8)],
        [(True,2),(True,2),(True,8)],
        [(True,4),(True,4),(True,4)], [(False,4),(True,4),(True,4)], [(True,4),(True,4),(False,4)],
        [(True,4),(True,4),(True,2),(True,2)], [(True,4),(True,2),(True,2),(True,4)], [(True,2),(True,2),(True,4),(True,4)],
        [(False,4),(True,4),(True,2),(True,2)],
        [(True,6),(True,4),(True,2)], [(True,6),(True,4),(True,2)], [(True,6),(True,4),(True,2)],
        [(True,4),(True,2),(True,4),(True,2)],[(True,4),(True,2),(True,4),(True,2)],
        [(True,10),(True,2)], [(True,10),(True,2)], [(True,10),(True,2)], [(True,10),(True,2)]
    ]

    opts[16] = [
        [(True,16)], 
        [(False,16)], 
        [(True,12),(True,4)], [(False,12),(True,4)], [(True,12),(False,4)],
        [(True,8),(True,8)], [(True,8),(False,8)], [(False,8),(True,8)], 
        [(True,8),(True,4),(True,4)],[(False,8),(True,4),(True,4)],
        [(True,4),(True,4),(True,8)],[(False,4),(True,4),(True,8)],[(True,4),(False,4),(True,8)],[(True,4),(True,4),(False,8)],
        [(True,4),(True,8),(True,4)],[(False,4),(True,8),(True,4)],[(True,4),(False,8),(True,4)],[(True,4),(True,8),(False,4)],[(True,4),(False,8),(True,4)],
        [(True,4),(True,4),(True,4),(True,4)],[(False,4),(True,4),(True,4),(True,4)],
        [(True,4),(False,4),(True,4),(True,4)],[(True,4),(True,4),(False,4),(True,4)],
        [(True,4),(True,4),(True,4),(False,4)],[(False,4),(True,4),(False,4),(True,4)],
        [(True,4),(False,4),(True,4),(False,4)],
        [(True,4),(True,4),(True,4),(True,2),(True,2)],[(False,4),(True,4),(True,4),(True,2),(True,2)],[(True,4),(False,4),(True,4),(True,2),(True,2)],[(True,4),(True,4),(False,4),(True,2),(True,2)],
        [(True,4),(True,4),(True,2),(True,2),(True,4)],[(False,4),(True,4),(True,2),(True,2),(True,4)],[(True,4),(True,4),(False,2),(True,2),(True,4)],
        [(True,4),(True,2),(True,2),(True,4),(True,4)],[(False,4),(True,2),(True,2),(True,4),(True,4)],[(True,4),(True,2),(True,2),(True,4),(False,4)],
        [(True,2),(True,2),(True,4),(True,4),(True,4)],[(True,2),(True,2),(True,4),(False,4),(True,4)],[(True,2),(True,2),(True,4),(True,4),(False,4)],

        [(True,8),(True,4),(True,2),(True,2)],[(False,8),(True,4),(True,2),(True,2)],[(True,8),(False,4),(True,2),(True,2)],
        [(True,8),(True,2),(True,2),(True,4)],[(False,8),(True,2),(True,2),(True,4)],
        [(True,4),(True,2),(True,2),(True,8)],[(False,4),(True,2),(True,2),(True,8)],
        [(True,2),(True,2),(True,8),(True,4)],[(True,2),(True,2),(True,8),(False,4)],
        [(True,2),(True,2),(True,4),(True,8)],[(True,2),(True,2),(True,4),(False,8)],
    
    ]
    durs = random.choice(opts[duration])
    return durs



##    opts[16] = [
##        [(True,16)], 
##        [(False,16)], 
##        [(True,12),(True,4)], [(False,12),(True,4)], [(True,12),(False,4)],
##        [(True,8),(True,8)], [(True,8),(False,8)], [(False,8),(True,8)], 
##        [(True,8),(True,4),(True,4)],[(False,8),(True,4),(True,4)],
##        [(True,4),(True,4),(True,8)],[(False,4),(True,4),(True,8)],[(True,4),(False,4),(True,8)],[(True,4),(True,4),(False,8)],
##        [(True,4),(True,8),(True,4)],[(False,4),(True,8),(True,4)],[(True,4),(False,8),(True,4)],[(True,4),(True,8),(False,4)],[(True,4),(False,8),(True,4)],
##        [(True,4),(True,4),(True,4),(True,4)],[(False,4),(True,4),(True,4),(True,4)],
##        [(True,4),(False,4),(True,4),(True,4)],[(True,4),(True,4),(False,4),(True,4)],
##        [(True,4),(True,4),(True,4),(False,4)],[(False,4),(True,4),(False,4),(True,4)],
##        [(True,4),(False,4),(True,4),(False,4)],
##        [(True,4),(True,4),(True,4),(True,2),(True,2)],[(False,4),(True,4),(True,4),(True,2),(True,2)],[(True,4),(False,4),(True,4),(True,2),(True,2)],[(True,4),(True,4),(False,4),(True,2),(True,2)],
##        [(True,4),(True,4),(True,2),(True,2),(True,4)],[(False,4),(True,4),(True,2),(True,2),(True,4)],[(True,4),(True,4),(False,2),(True,2),(True,4)],
##        [(True,4),(True,2),(True,2),(True,4),(True,4)],[(False,4),(True,2),(True,2),(True,4),(True,4)],[(True,4),(True,2),(True,2),(True,4),(False,4)],
##        [(True,2),(True,2),(True,4),(True,4),(True,4)],[(True,2),(True,2),(True,4),(False,4),(True,4)],[(True,2),(True,2),(True,4),(True,4),(False,4)],
##
##        [(True,8),(True,4),(True,2),(True,2)],[(False,8),(True,4),(True,2),(True,2)],[(True,8),(False,4),(True,2),(True,2)],
##        [(True,8),(True,2),(True,2),(True,4)],[(False,8),(True,2),(True,2),(True,4)],
##        [(True,4),(True,2),(True,2),(True,8)],[(False,4),(True,2),(True,2),(True,8)],
##        [(True,2),(True,2),(True,8),(True,4)],[(True,2),(True,2),(True,8),(False,4)],
##        [(True,2),(True,2),(True,4),(True,8)],[(True,2),(True,2),(True,4),(False,8)]
##    
####        [(True,6),(True,2),(True,6),(True,2)],[(True,6),(True,2),(True,6),(True,2)],[(True,6),(True,2),(True,6),(True,2)],
####        [(True,4),(True,4),(True,6),(True,2)],[(True,4),(True,4),(True,6),(True,2)],[(True,4),(True,4),(True,6),(True,2)],
####        [(True,8),(True,6),(True,2)],[(True,8),(True,6),(True,2)],[(True,8),(True,6),(True,2)],
####        [(True,6),(True,2),(True,8)],[(True,6),(True,2),(True,8)],[(True,6),(True,2),(True,8)],
####        
####        [(True,6),(True,2),(True,6),(True,2)],[(True,6),(True,2),(True,6),(True,2)],[(True,6),(True,2),(True,6),(True,2)],
####        [(True,4),(True,4),(True,6),(True,2)],[(True,4),(True,4),(True,6),(True,2)],[(True,4),(True,4),(True,6),(True,2)],
####        [(True,8),(True,6),(True,2)],[(True,8),(True,6),(True,2)],[(True,8),(True,6),(True,2)],
####        [(True,6),(True,2),(True,8)],[(True,6),(True,2),(True,8)],[(True,6),(True,2),(True,8)]
##        
##    ]
##    durs = random.choice(opts[duration])
##    return durs




##def harmonize_melody(segment, m):
##    ensemble = segment.movement.ensembles[segment.ensemble_number]
##    musicians = ensemble['melody_on_phrase_unison'] + ensemble['melody_on_phrase_type_unison']
##    melody_musician = random.choice(musicians)
##    
##    first_note = segment.notes[melody_musician][0].pitches
##    first_note = first_note[0]
##    previous_note = random.choice([first_note + 7, first_note - 7])
##    
##    prevs = [previous_note, previous_note]
##    for n in segment.notes[melody_musician]:
##        new_n = deepcopy_Event(n)
##        segment.notes[m].append(new_n)
##        if new_n.pitches:
##            pitch_to_harmonize = n.pitches
##            pitch_to_harmonize = pitch_to_harmonize[0]
##            register = segment.movement.musicians_by_name[m].instrument.register
##            harmony = get_at_microbeat(n.start, segment.harmonies)
##            harmony = harmony[0]
##            pitch = get_next_harmony_pitch(pitch_to_harmonize, prevs, harmony.pitches, harmony.scale, register)
##            new_n.pitches = [pitch]
##
##def get_next_harmony_pitch(pitch_to_harmonize, prevs, harmony, scale, register):
##
##    preferred_distance_from_previous = range(prevs[-1] - 5, prevs[-1] + 6)
##    acceptable_distance_from_previous = range(prevs[-1] - 8, prevs[-1] + 9)
##    acceptable_distance_from_two_previous = range(prevs[-2] - 7, prevs[-2] + 8)
##    acceptable_intervals = [3,4,5,7,8,9]
##
##    in_scale_preferred = []
##    in_scale = []
##    in_harmony_preferred = []
##    in_harmony = []
##    pretty_bad = []
##    last_resort = []
##    beyond_last_resort = []
##    
##    for p in register:
##        if ((pitch_to_harmonize - p) % 12) in acceptable_intervals:
##            beyond_last_resort.append(p)
##            if p in acceptable_distance_from_previous:
##                last_resort.append(p)                
##                if p in acceptable_distance_from_two_previous:
##                    pretty_bad.append(p)
##                    if p % 12 in scale:
##                        in_scale.append(p)
##                        if p in preferred_distance_from_previous:
##                            in_scale_preferred.append(p)
##
##                    if p % 12 in harmony:
##                        in_harmony.append(p)
##                        if p in preferred_distance_from_previous:
##                            in_harmony_preferred.append(p)
##
##    opts = in_harmony_preferred + in_harmony_preferred + \
##         in_harmony_preferred + in_scale_preferred + \
##         in_scale_preferred + in_scale_preferred + \
##         in_harmony + in_harmony + in_scale
##    if not opts:
##        opts += pretty_bad
##    if not opts:
##        opts += last_resort
##    if not opts:
##        opts += beyond_last_resort
##    if not opts:
##        opts += register    
##    return random.choice(opts)
##
##
##def melody_on_phrase_type_unison(segment, m):
##    segment.notes[m] = []
##    s = segment.start
##    for n in segment.melody_for_phrase_type_unison:
##        new_n = deepcopy_Event(n, new_start=s)
##        s += new_n.duration
##        segment.notes[m].append(new_n)
##            
##def melody_on_phrase_unison(segment, m):
##    segment.notes[m] = []
##    s = segment.start
##    for n in segment.melody_for_phrase_unison:
##        new_n = deepcopy_Event(n, new_start=s)
##        s += new_n.duration
##        segment.notes[m].append(new_n)
##def melody(segment):
##
##    num_half_bars = segment.duration/8
##    if num_half_bars == 4:
##        num_beg_half_bars = 1
##        num_end_half_bars = random.choice([1,1,2])
##    elif num_half_bars == 8:
##        num_beg_half_bars = random.choice([1,2,2,2])
##        num_end_half_bars = random.choice([1,2,2,3,3])
##    elif num_half_bars == 16:
##        num_beg_half_bars = random.choice([1,2,2,2,3,3,3,3,4])
##        num_end_half_bars = random.choice([1,2,3,3,4,4])
##    
##    if num_beg_half_bars:
##        beg_notes = get_melody_chunk(segment, num_beg_half_bars, segment.start)
##        rest_start = beg_notes[-1].next_event_start
##    else:
##        beg_notes = []
##        rest_start = segment.start
##    
##    end_start = segment.start + segment.duration - (num_end_half_bars*8)
##    end_notes = get_melody_chunk(segment, num_end_half_bars, end_start)
##    
##    rests_dur = end_start - rest_start
##    rests_half_notes = rests_dur/8
##    rests = []
##    s = rest_start
##    for counter in range(rests_half_notes):
##        r = Event(start=s, duration=8)
##        s += r.duration
##        r.pitches = []
##        rests.append(r)
##        harmony = get_at_microbeat(r.start, segment.harmonies)
##        harmony = harmony[0]
##        r.sharps_or_flats = harmony.sharps_or_flats
##
##    notes = beg_notes + rests + end_notes
##
##    return notes
##
##def get_melody_chunk(segment, num_beg_half_bars, start):
##    notes = []
##    # this is a generic melody for now
##    # use soprano range
##    # make nice rhythms
##    # match with lyrics somehow
##    register = range(-1,20)
##    prev_pitches = [random.choice(range(6,13))]
##    prev_pitches.append(prev_pitches[0] - 1)
##    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
##    s = start
##    for half_bar in range(num_beg_half_bars):
##        start_harmony = get_at_microbeat(s, segment.harmonies)
##        start_harmony = start_harmony[0]
##        upbeat_harmony = get_at_microbeat(s + 4, segment.harmonies)
##        upbeat_harmony = upbeat_harmony[0]
##        if start_harmony.pitches == upbeat_harmony.pitches:
##            durs = get_melody_rhythm_chunk(8)
##            for d in durs:
##                e = Event(start=s, duration=d)
##                s += e.duration
##                notes.append(e)    
##                if e.start == segment.start:
##                    e.rehearsal = True
##                    e.rehearsal_type = 'plain'
##                    e.rehearsal_text = rehearsal_text
##                e.sharps_or_flats = start_harmony.sharps_or_flats
##                
##                pitch = get_next_melody_pitch(prev_pitches, 
##                                                 start_harmony.pitches, 
##                                                 start_harmony.scale,
##                                                 register)
##                e.pitches = [pitch]
##                prev_pitches.append(pitch)
##        else:
##            durs = get_melody_rhythm_chunk(4)
##            for d in durs:
##                e = Event(start=s, duration=d)
##                s += e.duration
##                notes.append(e)    
##                if e.start == segment.start:
##                    e.rehearsal = True
##                    e.rehearsal_type = 'plain'
##                    e.rehearsal_text = rehearsal_text
##                e.sharps_or_flats = start_harmony.sharps_or_flats
##                pitch = get_next_melody_pitch(prev_pitches, 
##                                                 start_harmony.pitches, 
##                                                 start_harmony.scale,
##                                                 register)
##                e.pitches = [pitch]            
##                prev_pitches.append(pitch)
##                
##            durs = get_melody_rhythm_chunk(4)
##            for d in durs:
##                e = Event(start=s, duration=d)
##                s += e.duration
##                notes.append(e)    
##                if e.start == segment.start:
##                    e.rehearsal = True
##                    e.rehearsal_type = 'plain'
##                    e.rehearsal_text = rehearsal_text
##                e.sharps_or_flats = upbeat_harmony.sharps_or_flats
##                pitch = get_next_melody_pitch(prev_pitches, 
##                                                 start_harmony.pitches, 
##                                                 start_harmony.scale,
##                                                 register)
##                e.pitches = [pitch]       
##                prev_pitches.append(pitch)
##    return notes    
##
##def get_next_melody_pitch(prevs, harmony, scale, register):
##    scale_pitches = [p for p in register if p % 12 in scale]
##    chord_pitches = [p for p in register if p % 12 in harmony]
##    preferred = []
##    secondary = []
##    if prevs[-1] in scale_pitches: 
##        if random.choice([True, True, True, True, True, True, False]):
##            secondary.append(prevs[-1])
##        else:
##            preferred.append(prevs[-1])
##    if prevs[-2] in scale_pitches: preferred.append(prevs[-2])
##    if prevs[-1] + 1 in scale_pitches: preferred.append(prevs[-1] + 1)
##    if prevs[-1] + 2 in scale_pitches: preferred.append(prevs[-1] + 2)
##    if prevs[-1] + 3 in scale_pitches: preferred.append(prevs[-1] + 3)
##    if prevs[-1] + 4 in scale_pitches: secondary.append(prevs[-1] + 4)
##    if prevs[-1] + 5 in scale_pitches: secondary.append(prevs[-1] + 5)
##    if prevs[-1] - 1 in scale_pitches: preferred.append(prevs[-1] - 1)
##    if prevs[-1] - 2 in scale_pitches: preferred.append(prevs[-1] - 2)
##    if prevs[-1] - 3 in scale_pitches: preferred.append(prevs[-1] - 3)
##    if prevs[-1] - 4 in scale_pitches: secondary.append(prevs[-1] - 4)
##    if prevs[-1] - 5 in scale_pitches: secondary.append(prevs[-1] - 5)
##    if prevs[-1] in chord_pitches: 
##        if random.choice([True, True, True, True, False]):
##            secondary.append(prevs[-1])
##        else:
##            preferred.append(prevs[-1])
##    if prevs[-1] + 1 in chord_pitches: preferred.append(prevs[-1] + 1)
##    if prevs[-1] + 2 in chord_pitches: preferred.append(prevs[-1] + 2)
##    if prevs[-1] + 3 in chord_pitches: preferred.append(prevs[-1] + 3)
##    if prevs[-1] + 4 in chord_pitches: secondary.append(prevs[-1] + 4)
##    if prevs[-1] + 5 in chord_pitches: secondary.append(prevs[-1] + 5)
##    if prevs[-1] - 1 in chord_pitches: preferred.append(prevs[-1] - 1)
##    if prevs[-1] - 2 in chord_pitches: preferred.append(prevs[-1] - 2)
##    if prevs[-1] - 3 in chord_pitches: preferred.append(prevs[-1] - 3)
##    if prevs[-1] - 4 in chord_pitches: secondary.append(prevs[-1] - 4)
##    if prevs[-1] - 5 in chord_pitches: secondary.append(prevs[-1] - 5)
##    
##    if preferred:
##        pitch = random.choice(preferred)
##    elif secondary:
##        pitch = random.choice(secondary)        
##    else:
##        pitch = random.choice(scale_pitches + chord_pitches)        
##    
##    
##    return pitch
##
##def get_melody_rhythm_chunk(duration):
##    opts = {
##        4:[[4],[4],[2,2],[3,1],[4],[4],[2,2],[3,1],[2,1,1],[1,1,1,1]],
##        8:[[8],[8],[8],[8],[8],[8],[8],[6,2],[6,2],[3,5],[5,3],[4,4],[7,1],[4,2,2],[4,3,1]]
##    }
##    return random.choice(opts[duration])

    
    
def guitar_chords_on_phrase_type_unison(segment, m):
    if m == 'Ian':
        segment.notes[m] = []
        for n in segment.notes['Matt']:
            new_n = deepcopy_Event(n)
            segment.notes[m].append(new_n)

def guitar_chords_on_phrase_unison(segment, m):
    if m == 'Matt':
        segment.notes[m] = []
        guitar_chords(segment, m)
    if m == 'Ian':
        segment.notes[m] = []
        for n in segment.notes['Matt']:
            new_n = deepcopy_Event(n)
            segment.notes[m].append(new_n)
        
def guitar_chords_on_phrase_type(segment, m):
    pass
def guitar_chords_on_phrase(segment, m):
##    segment.notes[m] = []
##    guitar_chords(segment, m)
    segment.notes[m] = guitar_chords(segment, m)
    
def guitar_chords(segment, m):
    notes = []
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    prev_pitchclasses = None
    s = segment.start
    for measure in segment.measures:
        rhythm = get_measure_rhythm(measure, segment)
        for r in rhythm:
            n = Event(start=s, duration=r[1])
            s += n.duration
            notes.append(n)
            if n.start == segment.start:
                n.rehearsal = True
                n.rehearsal_type = 'plain'
                n.rehearsal_text = rehearsal_text
            
            if not r[0]:
                n.pitches = []
            else:
                h = get_at_microbeat(n.start, segment.harmonies)
                h = h[0]
                n.sharps_or_flats = h.sharps_or_flats
                if prev_pitchclasses != h.pitches:
##                    chord_options = get_fingerings_by_root_chordtype_range(
##                        h.root, 
##                        h.chordtype,
##                        segment.section_type.register[m][0],
##                        segment.section_type.register[m][-1]
##                    )
##                    fretboard_diagram, pitches = random.choice(chord_options)

                    n.pitches = h.pitches
                    #n.fretboard_diagram = fretboard_diagram
                    prev_pitches = n.pitches
                    prev_pitchclasses = h.pitches
 
                else:
                    n.pitches = prev_pitches
##    segment.notes[m] = notes
    return notes

def get_measure_rhythm(measure, segment):
    s1 = measure.start
    s2 = s1 + 4
    s3 = s2 + 4
    s4 = s3 + 4
    h1 = get_at_microbeat(s1, segment.harmonies)
    h1 = h1[0].pitches
    h2 = get_at_microbeat(s2, segment.harmonies)
    h2 = h2[0].pitches        
    h3 = get_at_microbeat(s3, segment.harmonies)
    h3 = h3[0].pitches
    h4 = get_at_microbeat(s4, segment.harmonies)
    h4 = h4[0].pitches
    
    a = h1 == h2
    b = h1 == h3
    c = h1 == h4
    d = h2 == h3
    e = h2 == h4
    f = h3 == h4
    
    if a and b and c and d and e and f:
        durs = [16]
    elif a and b and d and not c and not e and not f:
        durs = [12,4]
    elif a and f and not b and not c and not d and not e:
        durs = [8,8]
    elif d and e and f and not a and not b and not c:
        durs = [4,12]
    elif d and not a and not b and not c and not e and not f:
        durs = [4,8,4]
    
    rhythm = []
    for dur in durs:
        rs = get_guitar_rhythm_durs(dur)
        for r in rs:
            if type(r) == type([]):
                rhythm.extend(r)
            else:
                rhythm.append(r)
    return rhythm

def get_guitar_rhythm_durs(duration):
    opts = {}
    opts[4] = [ [(False,4)], [(True,4)] ]
    opts[8] = [ [(True,8)], [(True,8)], [(False,8)], [(True,4),(True,4)] ]
    opts[12] = [ [(True,12)], [(True,12)], [(True,12)], [(False,12)], [(True,8),(True,4)], [(True,8),(True,4)] ]
    opts[16] = [
        [(True,16)], [(True,16)], [(True,16)], [(True,16)], [(True,16)], [(True,16)], [(True,16)], [(True,16)],
        [(False,16)], [(False,16)],
        [(True,12),(True,4)], [(True,12),(True,4)], [(True,12),(True,4)], [(True,12),(True,4)],
        [(True,8),(True,8)], [(True,8),(True,8)], [(True,8),(True,8)], 
        [(True,8),(True,4),(True,4)]
    ]
    durs = random.choice(opts[duration])
    return durs



def drone(segment, m):    
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    e = Event(start=segment.start, duration=segment.duration)
    e.pitches = segment.movement.drone_pitches
    harmony = get_at_microbeat(e.start, segment.harmonies)
    harmony = harmony[0]
    e.sharps_or_flats = harmony.sharps_or_flats    
    if e.start == segment.start:
        e.rehearsal = True
        e.rehearsal_type = 'plain'
        e.rehearsal_text = rehearsal_text 
    segment.notes[m] = [e]

def resting(segment, m):
    segment.notes[m] = []
    for meas in segment.measures:
        r = Event(start=meas.start, duration=meas.duration)
        r.pitches = []
        segment.notes[m].append(r)

def beg_and_end_chords_sustained_on_phrase_type(segment, m):
    segment.notes[m] = segment.beg_and_end_chords_sustained_on_phrase_type[m]
def beg_and_end_chords_sustained_on_phrase(segment, m):
    segment.notes[m] = beg_and_end_chords_sustained(segment, m)
    
def beg_and_end_chords_sustained(segment, m):
    num_harms = len(segment.harmonies)
    if num_harms > 6:
        num_beg_chords = random.choice([1,1,1,2,2,3])
        num_end_chords = random.choice([1,1,1,1,2,2,2,3])
    elif num_harms > 4:
        num_beg_chords = random.choice([1,1,1,1,2,2,3])
        num_end_chords = random.choice([0,1,1,1,1,2,2,2,2])
    elif num_harms > 2:
        num_beg_chords = 1
        num_end_chords = random.choice([1,1,1,0])
    elif num_harms <= 2:
        num_beg_chords = 1
        num_end_chords = 0
    
    beg_harms = segment.harmonies[:num_beg_chords]
    beg_chords = get_chord_chunk(segment, m, beg_harms)    

    if num_end_chords == 0:
        end_chords = []        
        
        mid_harms = segment.harmonies[num_beg_chords:]
        rests = []
        for h in mid_harms:
            r = Event(start=h.start, duration=h.duration)
            r.pitches = []
            r.sharps_or_flats = h.sharps_or_flats
            rests.append(r)
    else:
        end_harms = segment.harmonies[-num_end_chords:]
        end_chords = get_chord_chunk(segment, m, end_harms)

        mid_harms = segment.harmonies[num_beg_chords:-num_end_chords]
        rests = []
        for h in mid_harms:
            r = Event(start=h.start, duration=h.duration)
            r.pitches = []
            r.sharps_or_flats = h.sharps_or_flats
            rests.append(r)
    
    return beg_chords + rests + end_chords


    
    
    
    
    
def get_durs_for_rest_across_measures(start, dur, segment):
    print 'start:', start, 'dur:', dur
    durs = []
    measures = []
    # get measures starting during rest
    for mb in range(start, start + dur):
        print mb
        measure = get_at_microbeat(mb, segment.measures)
        measure = measure[0]
        if measure not in measures:
            measures.append(measure)
    for m in measures:
        print 'Measure Start:', m.start
    measure_starts = [m.start for m in measures if m.start > start and m.start < start + dur]
    prev = start
    for st in measure_starts:
        d = st - prev
        durs.append(d)
        
    last_d = start + dur - measure_starts[-1]
    durs.append(last_d)

    return durs
    
    
    
def get_chord_chunk(segment, m, harms):
    
    musician = segment.movement.musicians_by_name[m]
    register = musician.instrument.conservative_register
    
    events = []
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    prev_pitches = []    
    for h in harms:
        n = Event(start=h.start, duration=h.duration)
        events.append(n)
        if n.start == segment.start:
            n.rehearsal = True
            n.rehearsal_type = 'plain'
            n.rehearsal_text = rehearsal_text         
        n.sharps_or_flats = h.sharps_or_flats  
        
##        pitch_options = [p for p in segment.section_type.register[m] if p%12 in h.pitches]
        pitch_options = [p for p in register if p%12 in h.pitches]
        num_notes = random.choice(segment.section_type.keyboard_thickness[m])        
        preferred_pitches = list(set(prev_pitches) & set(pitch_options))        
        n.pitches = []
        for counter in range(num_notes):
            for px in range(-7, 8):
                if px in n.pitches:
                    preferred_pitches = [pp for pp in preferred_pitches if pp > 7]
                    pitch_options = [pp for pp in pitch_options if pp > 7]
                    
            preferred = random.choice([True, True, True, False])
            if preferred:
                if preferred_pitches:
                    p = random.choice(preferred_pitches)
                    if p not in n.pitches:
                        n.pitches.append(p)
                    i = preferred_pitches.index(p)
                    del preferred_pitches[i]                
                    if p in pitch_options:
                        i = pitch_options.index(p)
                        del pitch_options[i]
                else:
                    if pitch_options:
                        p = random.choice(pitch_options)
                        if p not in n.pitches:
                            n.pitches.append(p)
                        i = pitch_options.index(p)
                        del pitch_options[i]                
                        if p in preferred_pitches:
                            i = preferred_pitches.index(p)
                            del preferred_pitches[i]
            else:
                if pitch_options:
                    p = random.choice(pitch_options)
                    if p not in n.pitches:
                        n.pitches.append(p)
                    i = pitch_options.index(p)
                    del pitch_options[i]                
                    if p in preferred_pitches:
                        i = preferred_pitches.index(p)
                        del preferred_pitches[i]
                else:
                    if preferred_pitches:
                        p = random.choice(preferred_pitches)
                        if p not in n.pitches:
                            n.pitches.append(p)
                        i = preferred_pitches.index(p)
                        del preferred_pitches[i]                
                        if p in pitch_options:
                            i = pitch_options.index(p)
                            del pitch_options[i]                    
        prev_pitches = n.pitches
    print n.pitches
    return events   
    
    
    
def chords_sustained_on_phrase_type(segment, m):
    segment.notes[m] = segment.chords_sustained_on_phrase_type[m]

def chords_sustained_on_phrase(segment, m):
    segment.notes[m] = chords_sustained(segment, m)
 
def chords_sustained(segment, m):
    
    musician = segment.movement.musicians_by_name[m]
    register = musician.instrument.conservative_register 
    
    strumming = segment.section_type.strumming[m]
        
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    prev_pitches = []
    notes = []
    for h in segment.harmonies:
        num_notes = random.choice(segment.section_type.keyboard_thickness[m])
        pitches = chord_get_pitches(h, num_notes, prev_pitches, register)
        
        if strumming:
            rhythm = get_chord_rhythm(h.duration)
        else:
            rhythm = [h.duration]
        s = h.start
        for r in rhythm:
            n = Event(start=s, duration=r)
            s += r
            if n.start == segment.start:
                n.rehearsal = True
                n.rehearsal_type = 'plain'
                n.rehearsal_text = rehearsal_text         
            n.sharps_or_flats = h.sharps_or_flats
            n.pitches = pitches
            prev_pitches = n.pitches
            notes.append(n)    
            

##        num_notes = random.choice(segment.section_type.keyboard_thickness[m])
##        n.pitches = chord_get_pitches(h, num_notes, prev_pitches, register)                  
##        prev_pitches = n.pitches        
##        notes.append(n)    
    return notes

def chord_get_pitches(h, num_notes, prev_pitches, register):
    pitch_options = [p for p in register if p%12 in h.pitches]
    pitches = random.sample(pitch_options, num_notes)
    return pitches
        

##def chord_get_pitches(h, num_notes, prev_pitches, register):
##    pitches = []
##    pitch_options = [p for p in register if p%12 in h.pitches]
##    
##    preferred_scaledegrees = [0,7,5]
##    preferred_pitchclasses = [h.root+pc for pc in preferred_scaledegrees]
##    preferred_pitches = [p for p in register if p%12 in preferred_pitchclasses]
##    acceptable_prev_pitches = list(set(prev_pitches) & set(pitch_options))
##    preferred_pitches = acceptable_prev_pitches + preferred_pitches
##    
##    for counter in range(num_notes):
##        preferred = random.choice([True, True, True, False])
##        if preferred:
##            if preferred_pitches:
##                p = random.choice(preferred_pitches)
##                
##                if p not in pitches:
##                    pitches.append(p)
##                i = preferred_pitches.index(p)
##                del preferred_pitches[i]                
##                if p in pitch_options:
##                    i = pitch_options.index(p)
##                    del pitch_options[i]
##            else:
##                if pitch_options:
##                    p = random.choice(pitch_options)
##                    if p not in pitches:
##                        pitches.append(p)
##                    i = pitch_options.index(p)
##                    del pitch_options[i]                
##                    if p in preferred_pitches:
##                        i = preferred_pitches.index(p)
##                        del preferred_pitches[i]
##        else:
##            if pitch_options:
##                p = random.choice(pitch_options)
##                if p not in pitches:
##                    pitches.append(p)
##                i = pitch_options.index(p)
##                del pitch_options[i]                
##                if p in preferred_pitches:
##                    i = preferred_pitches.index(p)
##                    del preferred_pitches[i]
##            else:
##                if preferred_pitches:
##                    p = random.choice(preferred_pitches)
##                    if p not in pitches:
##                        pitches.append(p)
##                    i = preferred_pitches.index(p)
##                    del preferred_pitches[i]                
##                    if p in pitch_options:
##                        i = pitch_options.index(p)
##                        del pitch_options[i]
##    return pitches


#---------------------------------------
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
    keyboardists = ['Quentin', 'Phil']#, 'Will']
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
        max_register = max_register[13:]
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
    ['Emma', 'Paul', 'Katie', 'Christine', 'Michael', 'Mark', 'James']
    segment.keyboard_thickness = {}
    segment.keyboard_thickness['Emma'] = [1]
    segment.keyboard_thickness['Paul'] = [1]
    segment.keyboard_thickness['Katie'] = [2,3,4]
    segment.keyboard_thickness['Christine'] = [1]    
    segment.keyboard_thickness['Michael'] = [1]
    segment.keyboard_thickness['Mark'] = [2,3,4,5,6]
    segment.keyboard_thickness['James'] = [1]

 
def make_keyboard_notes(segment, m):
    rehearsal_text = '{0}{1}'.format(segment.section_type.name, segment.name)
    segment.movement.notes[m] = []
    s = segment.start
    prev_pitches = []
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
        
        preferred_pitches = list(set(prev_pitches) & set(pitch_options))
        note.pitches = []
        for n in range(num_notes):
            preferred = random.choice([True, True, True, False])
            if preferred:
                if preferred_pitches:
                    p = random.choice(preferred_pitches)
                    note.pitches.append(p)
                    i = preferred_pitches.index(p)
                    del preferred_pitches[i]                
                    if p in pitch_options:
                        i = pitch_options.index(p)
                        del pitch_options[i]
                else:
                    if pitch_options:
                        p = random.choice(pitch_options)
                        note.pitches.append(p)
                        i = pitch_options.index(p)
                        del pitch_options[i]                
                        if p in preferred_pitches:
                            i = preferred_pitches.index(p)
                            del preferred_pitches[i]
            else:
                if pitch_options:
                    p = random.choice(pitch_options)
                    note.pitches.append(p)
                    i = pitch_options.index(p)
                    del pitch_options[i]                
                    if p in preferred_pitches:
                        i = preferred_pitches.index(p)
                        del preferred_pitches[i]
                else:
                    if preferred_pitches:
                        p = random.choice(preferred_pitches)
                        note.pitches.append(p)
                        i = preferred_pitches.index(p)
                        del preferred_pitches[i]                
                        if p in pitch_options:
                            i = pitch_options.index(p)
                            del pitch_options[i]                    
        prev_pitches = note.pitches
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
            make_horns_parts(segment, lead, 'Katie')
            make_horns_parts(segment, backup_duo, 'Beth')
            make_horns_parts(segment, backup_duo, 'Jason')
        else:
            make_backing_vocals(segment, backup_duo, 'Katie')
            make_backing_vocals(segment, backup_duo, 'Beth')
            make_backing_vocals(segment, lead, 'Jason')
            
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
def make_report(movement):
    tem = 'tempo: {0}\n'.format(movement.tempo_bpm)
    dur_16 = 'duration in sixteenth notes: {0}\n'.format(movement.duration)
    dur_sec = 'duration in seconds: {0}\n'.format(movement.duration_seconds)
    schiz = 'schizoid harmony: {0}\n'.format(movement.schizoid_harmony)
    order = '{0}\n'.format(movement.segment_order)
    movement.report = [tem,dur_16,dur_sec,schiz,order]
    movement.report.append('\n')     
    double_line = '='*40
    single_line = '-'*20
    for phrase in movement.phrases:
        pn = '{0} Ens. {1}\n'.format(phrase.full_name, phrase.ensemble_number)
        movement.report.append(pn)
    movement.report.append('\n')  
    for phrase in movement.phrases:
        pn = '\n{0} Ensemble {1}\n'.format(phrase.full_name, phrase.ensemble_number)
        movement.report.append(pn)        
        for r, h in zip(phrase.harmonic_rhythm, phrase.harmonies):
            f = ' {0:<5}{1:<15}{2}\n'.format(r, h.pitches, h.scale)
            movement.report.append(f)

            
    role_order = [
        'melody_on_phrase_type_unison',
        'melody_on_phrase_unison',
        'harmonize_melody',
        'simple_melody_on_phrase_type_unison',
        'simple_melody_on_phrase_unison',
        'harmonize_simple_melody',
        'baritone_simple_melody_on_phrase_type_unison',
        'baritone_simple_melody_on_phrase_unison',
        'baritone_harmonize_simple_melody',
        'chords_sustained_on_phrase_type',
        'chords_sustained_on_phrase',
        'beg_and_end_chords_sustained_on_phrase_type',
        'beg_and_end_chords_sustained_on_phrase',
        'guitar_chords_on_phrase_type_unison',
        'guitar_chords_on_phrase_unison',
        'guitar_chords_on_phrase_type',
        'guitar_chords_on_phrase',
        #'drone',
        'resting'
    ]

    movement.report.append('\n') 
    movement.report.append('\n') 
    for ens_num in movement.ensembles:
        ens = movement.ensembles[ens_num]
        movement.report.append('\n') 
        for role in role_order:
            eee = '{0:<46}{1}\n'.format(role, ens[role])
            movement.report.append(eee)
    
    movement.report = ''.join(movement.report)
    print movement.report
    
#---------------------------------------
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
        #self.write_file(movement.report, 'form.txt')
        
        self.tempo_duration = 4
        self.tempo_bpm = movement.tempo_bpm
        self.duration_denominator = 16

        self.make_meter(movement)
        BaseMovement.ly_closeout(self)

    def choose_ensemble(self):
        self.musicians = []

        emma = Musician(SopranoSaxophone())
        emma.name = 'Emma'
        self.musicians.append(emma)

        paul = Musician(Trumpet())
        paul.name = 'Paul'
        self.musicians.append(paul)

        katie = Musician(CasioSK1())
        katie.name = 'Katie'
        self.musicians.append(katie)

        christine = Musician(Flute())
        christine.name = 'Christine'
        self.musicians.append(christine)        
        
        michael = Musician(Guitar())
        michael.name = 'Michael'
        michael.instrument.name = 'Acoustic Guitar'
        self.musicians.append(michael)
        
        mark = Musician(Piano())
        mark.name = 'Mark'
        self.musicians.append(mark)        
        
        james = Musician(Bass())
        james.name = 'James'
        james.instrument.name = 'Double Bass'
        self.musicians.append(james)

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











