from isa.inst import *
import numpy as np
import math

class Vsoxsegxeix_v(Inst):
    name = 'vsoxsegxeix.v'

    def golden(self):
        vl = self['vs2'].size
        vd_size = vl * self['nfields']
        vd = np.zeros( vd_size, dtype=self['vs3'].dtype )
        for no in range( 0, self['vs2'].size ):
            if 'mask' in self:
                mask = ( self['mask'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1
            else:
                mask = 1
            if mask == 1:
                for idx in range( 0, self['nfields']):
                    vd[int( self['vs2'][no]/self['vs3'].itemsize + idx)] = self['vs3'][ no*self['nfields']+idx]

        return vd
