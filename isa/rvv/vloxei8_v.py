from isa.inst import *
import numpy as np
import math

class Vloxei8_v(Inst):
    name = 'vloxei8.v'

    def golden(self):

        vd = np.zeros( self['rs1'].size, dtype=self['rs1'].dtype )
        for no in range( 0, self['vs2'].size ):
            vd[no] = self['rs1'][int( self['vs2'][no]/self['rs1'].itemsize )]

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd
