from ...isa.inst import *
import numpy as np

class Fcvt_w_s(Inst):
    name = 'fcvt.w.s'

    def golden(self):
        if 'val1' in self.keys():          
            if self['val1'] < -(1<<31) or np.isneginf(self['val1']):
                return -(1<<31)
            if self['val1'] > ((1<<31)-1) or np.isposinf(self['val1']) or np.isnan(self['val1']):
                return (1<<31)-1
            return int(self['val1'])
       
