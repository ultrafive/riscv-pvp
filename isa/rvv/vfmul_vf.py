from isa.inst import *
import numpy as np

class Vfmul_vf(Inst):
    name = 'vfmul.vf'

    def golden(self):
        if 'v0' in self:
            mask = []
            for no in range(0, self['rs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, self['rs1'].astype( self['rs2'].dtype ) * self['rs2'], self['orig'])
        else:
            return self['rs1'].astype( self['rs2'].dtype ) * self['rs2']
