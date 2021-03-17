from isa.inst import *
import numpy as np

class Vemax_mv(Inst):
    name = 'vemax.mv'

    def golden( self ):
        if 'rs1' in self.keys():
            return np.maximum( self['rs1'], self['vs2'])