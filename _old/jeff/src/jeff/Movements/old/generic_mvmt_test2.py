from BasePiece.BaseEvent import Event, BaseEvent
from copy_Event import deepcopy_Event

class Top_Level(BaseEvent):
    def __init__(self, name):
        self.name = name
        BaseEvent.__init__(self)
        

class Section(BaseEvent):
    pass

class Phrase(BaseEvent):
    pass

def make_subsections(section, subsections_order):
    subsection_type_names = list(set(subsections_order))
    subsection_types = {}
    for name in subsection_type_names:
        section_type = make_section(name, section)
        subsection_types[name] = section_type
    subsections = []
    for subsection_name in subsections_order:
        subsection = deepcopy_Event(subsection_types[subsection_name])
        subsections.append(subsection)
    
    return subsections

def make_section(name, parent=None):
    section = BaseEvent()
    section.name = name
    
    return section
    
if __name__ == '__main__':
    movement = Top_Level('movement')
    sections_order = ['a', 'a', 'b', 'a', 'b']
    
    movement.sections = make_subsections(movement, sections_order)
    
    
    
    for section in movement.sections:
        print section.name