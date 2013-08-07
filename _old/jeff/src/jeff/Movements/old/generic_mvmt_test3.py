from BasePiece.BaseEvent import Event, BaseEvent
from copy_Event import deepcopy_Event
import random

movement = BaseEvent(start=0)

movement.segment_order_options = [
    ['I', 'I', 'II', 'I', 'III', 'III', 'II', 'I'],
    ['I', 'I', 'II', 'I', 'III', 'III'],
    ['I', 'I', 'I', 'II', 'III', 'III', 'II', 'I'],
    ['I', 'II', 'I', 'II', 'III', 'III', 'II', 'I'],
    ['I', 'II', 'I', 'II', 'III', 'III', 'III', 'I'],
    ['I', 'II', 'I', 'III', 'III', 'III', 'II', 'I']
]

movement.segment_order = random.choice(movement.segment_order_options)
movement.segment_type_names = list(set(movement.segment_order))

print movement.segment_order
print movement.segment_type_names


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
for section_type_name in movement.segment_type_names:
    section_type = BaseEvent(start=0, duration=128)
    movement.segment_types[section_type_name] = section_type    
    
    section_type.name = section_type_name
    
    num_of_segments = random.choice([1,2,4])
    section_type.segment_order = random.choice(movement.subsegment_order_options[num_of_segments])
    section_type.segment_type_names = list(set(section_type.segment_order))
    
    print section_type.segment_order
    print section_type.segment_type_names    
    
    section_type.segment_types = {}
    for phrase_type_name in section_type.segment_type_names:
        d = section_type.duration/num_of_segments
        phrase_type = BaseEvent(start=0, duration=d)
        section_type.segment_types[phrase_type_name] = phrase_type    
        
        phrase_type.name = phrase_type_name
        
        print '\t', phrase_type.name, phrase_type.duration
        

        
        
        


    
    
    
    
    
    
    
    