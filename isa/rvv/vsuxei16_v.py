from isa.inst import *
import numpy as np
import math

class Vsuxei16_v(Inst):
    name = 'vsuxei16.v'

    def golden(self):

        vd = np.zeros( self['vs2'].size, dtype=self['vs3'].dtype )
        for no in range( 0, self['vs2'].size ):
            vd[int( self['vs2'][no]/self['vs3'].itemsize )] = self['vs3'][no]

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['rs1'])
        else:
            return vd
