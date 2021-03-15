from isa.inst import *
import numpy as np

class Veemacc_mv(Inst):
    name = 'veemacc.mv'

    def golden(self):
        if 'rs1' in self.keys():
            rd = np.sum( self['rs1'] * self['rs2'], axis = self['dim'] )
            rd = np.atleast_1d( rd )
            return rd