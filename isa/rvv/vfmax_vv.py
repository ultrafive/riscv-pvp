from isa.inst import *
import numpy as np

class Vfmax_vv(Inst):
    name = 'vfmax.vv'

    def golden(self):
        if 'rs2' not in self:
            return self['rs1']
        elif 'v0' in self:
            mask = []
            for no in range(0, self['rs1'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, np.maximum(self['rs1'], self['rs2']), self['orig'])            
        else:
            return np.maximum(self['rs1'], self['rs2'])
