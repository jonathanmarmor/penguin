from piece.BasePiece import BasePiece
from piece.BaseEvent import BaseEvent
from Movements.MvmtType3 import MvmtType3

class Piece(BasePiece):
    def __init__(self):
        self.name = __file__.rstrip('.py')
        BasePiece.__init__(self, self.name)

        mvmt_types = {
            3:MvmtType3
        }
        mvmts_order = [3]#,3,3,3,3]

        seq_nums = [1]#,2,3,4,5]
        section_type_names = {
            3:'I'
        }

        for mvmt_type, seq_num in zip(mvmts_order, seq_nums):
            self.make_a_movement(seq_num, section_type_names, mvmt_type, mvmt_types)
#            self.safety_wrapper(seq_num, section_type_names, mvmt_type, mvmt_types)
            
        print 'going into BasePiece.closeout...',
        BasePiece.closeout(self)
        print 'done'

    def safety_wrapper(self, seq_num, section_type_names, mvmt_type, mvmt_types):
        try:
            
            self.make_a_movement(seq_num, section_type_names, mvmt_type, mvmt_types)
##        except KeyError:
##            print 'KeyError!'
        except Exception:
            self.safety_wrapper(seq_num, section_type_names, mvmt_type, mvmt_types) 
  
    def make_a_movement(self, seq_num, section_type_names, mvmt_type, mvmt_types):
        print 'attempt'
        mvmt_name = 'Movement{0}'.format(seq_num)
        if seq_num < 10:
            folder_name = 'Mv_0{0}'.format(seq_num)
            file_name_prefix = 'Mv_0{0}'.format(seq_num)
        else:
            folder_name = 'Mv_{0}'.format(seq_num)
            file_name_prefix = 'Mv_{0}'.format(seq_num)              
        main_title = 'Movement {0}'.format(seq_num)
        subtitle = ''#'Type {0}'.format(section_type_names[mvmt_type])            
        
        mv = mvmt_types[mvmt_type](self, mvmt_name, seq_num, folder_name, file_name_prefix, main_title, subtitle)        

def run_dogstar(start_directory):
    try:
        os.chdir(start_directory)
        new_piece = Piece()
    except Exception:
        run_dogstar(start_directory)

import os
start_directory = os.getcwd()
for x in range(1):
    run_dogstar(start_directory)

##new_piece = Piece()