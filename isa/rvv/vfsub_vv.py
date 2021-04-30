from isa.inst import *
import numpy as np

class Vfsub_vv(Inst):
    name = 'vfsub.vv'

    def golden(self):
        if 'vs2' not in self:
            return self['vs1'] - self['vs1']
        elif 'v0' in self:
            mask = []
            for no in range(0, self['vs1'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, self['vs2'] - self['vs1'], self['orig'])            
        else:
            return self['vs2'] - self['vs1']
