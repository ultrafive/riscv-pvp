from ...isa.inst import *
import numpy as np
class Fcvt_wu_s(Inst):
    name = 'fcvt.wu.s'

    def golden(self):
        if 'val1' in self.keys(): 
            if self['val1'] < 0 or np.isneginf(self['val1']):
                return 0
            if self['val1'] > ((1<<32)-1) or np.isposinf(self['val1']) or np.isnan(self['val1']):
                return (1<<32)-1
            return int(self['val1'])
       
