from BasePiece.BaseEvent import Event, BaseEvent
from copy_Event import deepcopy_Event
import random

def movement_init():
    movement = BaseEvent(start=0)
    
    
    movement.top_level_options = [
        ['I', 'I', 'II', 'I', 'III', 'III', 'II', 'I'],
        ['I', 'I', 'II', 'I', 'III', 'III'],
        ['I', 'I', 'I', 'II', 'III', 'III', 'II', 'I'],
        ['I', 'II', 'I', 'II', 'III', 'III', 'II', 'I'],
        ['I', 'II', 'I', 'II', 'III', 'III', 'III', 'I'],
        ['I', 'II', 'I', 'III', 'III', 'III', 'II', 'I']
    ]
    movement.second_level_options = {
        'I': {
            1: [['A']],
            2: [['A','A']],
            4: [['A','A','A','A'],['A','A','B','A'],['A','A','B','B'],
                ['A','B','A','B'],['A','A','A','B'],['A','B','B','B'],
                ['A','B','B','C'],['A','B','A','C'],['A','B','C','A'], 
                ['A','B','B','A'],['A','A','B','C'],['A','B','A','A'],
                ['A','B','C','B'],['A','B','C','C']]
        }
    }
    movement.second_level_options['II'] = second_level_options['I']
    movement.second_level_options['III'] = second_level_options['I']
    
    

def make_form():
    
    

    

    
    
    movement.sections_order = random.choice(top_level_options)
    section_type_names = list(set(movement.sections_order))
    
    movement.section_types = {}
    for name in section_type_names:
        section_type = BaseEvent()
        section_type.duration = 128
        section_type.name = name
        num_sections = random.choice([1,2,4])
        section_type.sections_order = random.choice(second_level_options[name][num_sections])
        section_type.section_type_names = list(set(section_type.sections_order))
        movement.section_types[name] = section_type
        
        


    for n in movement.sections_order:
        print movement.section_types[n].name
        for x in movement.section_types[n].sections_order:
            print '\t', x
    
 

def make_movement(name):
    movement = BaseEvent(start=0)
    movement.name = name    
    return movement    

def make_section_types(movement):
    section_type_names = list(set(movement.sections_order))
    movement.section_types = {}
    for name in section_type_names:
        section_type = make_section_type(name, movement)
        movement.section_types[name] = section_type

def make_section_type(name, movement):
    section_type = BaseEvent(start=0)
    section_type.name = name    
    return section_type
    
 
def make_phrase_types(section):
    phrase_type_names = list(set(section.phrases_order))
    phrase_types = {}
    for name in phrase_type_names:
        phrase_type = make_phrase_type(name, section)
        phrase_types[name] = phrase_type
    return phrase_types

def make_phrase_type(name, section):
    phrase_type = BaseEvent(start=0)
    phrase_type.name = name    
    return phrase_type


def make_sections(movement):
    """ take section types and make sections in order by making exact copies"""
    movement.sections = []
    for section_name in movement.sections_order:
        section = deepcopy_Event(movement.section_types[section_name])
        movement.sections.append(section)
    

def make_whole_thing():
    movement_init()
        
        
if __name__ == '__main__':
    
    
##    movement = make_section('movement')
##    movement.sections_order = ['I', 'I', 'II', 'I', 'III', 'III']
##    make_section_types(movement)
##    
##    for section_type in movement.section_types:
##        section_type.phrases_order = random.choice([['1', '1', '2' '2'],['1','2','1','2'], ['1','1'], ['1']])
##        section.phrase_types = make_phrase_types(section)
##    
##    
##    
##    for section in movement.sections:
##        print section.name
##        for subsection in section.subsections:
##            print '\t', subsection.name
    make_form()