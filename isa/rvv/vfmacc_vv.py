from isa.inst import *
import numpy as np

class Vfmacc_vv(Inst):
    name = 'vfmacc.vv'

    def golden(self):
        if 'v0' in self:
            mask = []
            for no in range(0, self['vs1'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)          
            return np.where( mask == 1, self['vs1'] * self['vs2'] + self['vd'], self['vd'])
        else:
            return self['vs1'] * self['vs2'] + self['vd']
