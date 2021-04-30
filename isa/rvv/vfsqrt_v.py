from isa.inst import *
import numpy as np

class Vfsqrt_v(Inst):
    name = 'vfsqrt.v'

    def golden(self):
        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, np.sqrt( self['vs2'] ), self['orig'])
        else:
            return np.sqrt( self['vs2'] )
