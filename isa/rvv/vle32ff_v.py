from isa.inst import *
import numpy as np
import math

class Vle32ff_v(Inst):
    name = 'vle32ff.v'

    def golden(self):

        vd = self['rs1'].copy()

        if 'v0' in self:
            mask = []
            for no in range(0, self['rs1'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd
