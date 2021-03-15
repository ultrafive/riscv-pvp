from isa.inst import *
import numpy as np

class Veemacc_mf(Inst):
    name = 'veemacc.mf'

    def golden(self):
        if 'rs1' in self.keys():
            rd = np.sum( self['rs1'] * ( self['rs2'].astype('float16') ), axis = self['dim'] )
            rd = np.atleast_1d( rd )
            return rd