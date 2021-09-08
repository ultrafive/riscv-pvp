from ...isa.inst import *
import numpy as np
class Fcvt_l_s(Inst):
    name = 'fcvt.l.s'

    def golden(self):
        if 'val1' in self.keys(): 
            if self['val1'] < -(1<<63) or np.isneginf(self['val1']):
                return -(1<<63)
            if self['val1'] > ((1<<63)-1) or np.isposinf(self['val1']) or np.isnan(self['val1']):
                return (1<<63)-1
            return int(self['val1'])
       
