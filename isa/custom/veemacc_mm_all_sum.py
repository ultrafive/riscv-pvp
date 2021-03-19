from isa.inst import *
import numpy as np

class Veemacc_mm_all_sum(Inst):
    name = 'veemacc.mm'

    def golden(self):
        if 'rs1' in self.keys():
            rd = np.sum( self['rs1'] * self['rs2'], axis = None )
            rd = np.atleast_1d( rd )
            return rd.astype( np.float32 )