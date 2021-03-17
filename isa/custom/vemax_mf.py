from isa.inst import *
import numpy as np

class Vemax_mf(Inst):
    name = 'vemax.mf'

    def golden( self ):
        if 'rs1' in self.keys():
            return np.maximum( self['rs1'], self['rs2'].astype('float16') )