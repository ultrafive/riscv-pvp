from isa.inst import *
import numpy as np

class Vemax_all(Inst):
    name = 'vemax.m'

    def golden( self ):
        if 'rs1' in self.keys():
            rd = np.amax( self['rs1'] )
            return np.array( rd ).astype( np.float32 )