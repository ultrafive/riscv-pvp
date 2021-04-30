from isa.inst import *
import numpy as np

class Vfnmsac_vf(Inst):
    name = 'vfnmsac.vf'

    def golden(self):
        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, - self['vs2'] * self['rs1'].astype(self['vs2'].dtype) + self['vd'], self['vd'])
        else:
            return - self['vs2'] * self['rs1'].astype(self['vs2'].dtype) + self['vd']
