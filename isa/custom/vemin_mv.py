from isa.inst import *
import numpy as np

class Vemin_mv(Inst):
    name = 'vemin.mv'

    def golden( self ):
        if 'rs1' in self.keys():
            return np.minimum( self['rs1'], self['vs2'])