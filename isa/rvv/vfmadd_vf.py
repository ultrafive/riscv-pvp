from isa.inst import *
import numpy as np

class Vfmadd_vf(Inst):
    name = 'vfmadd.vf'

    def golden(self):
        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, self['vd'] * self['rs1'].astype(self['vs2'].dtype) + self['vs2'], self['vd'])
        else:
            return self['vd'] * self['rs1'].astype(self['vs2'].dtype) + self['vs2']
