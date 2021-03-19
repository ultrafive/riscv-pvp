from isa.inst import *
import numpy as np

class Vemin_m_all(Inst):
    name = 'vemin.m'

    def golden( self ):
        if 'rs1' in self.keys():
            rd = np.amin( self['rs1'] )
            return np.array( rd ).astype( np.float32 )