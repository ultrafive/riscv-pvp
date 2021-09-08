from ...isa.inst import *
import numpy as np

class Fmin(Inst):
    name = 'fmin.s'

    def golden(self):
        if self['rs1'] == -0.0 and self['rs2'] == 0.0:
            return -0.0
        if self['rs2'] == -0.0 and self['rs1'] == 0.0:
            return -0.0      
        if self['rs1'] == 'NaN' and self['rs2'] == 'NaN'  :
            return 0x7fc00000
        if self['rs1'] == 'NaN':
            return self['rs2']
        if self['rs2'] == 'NaN':
            return self['rs1']
        
        return min( self['rs1'], self['rs2'] )
       
