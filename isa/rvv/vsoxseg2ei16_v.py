from isa.inst import *
import numpy as np
import math

class Vsoxseg2ei16_v(Inst):
    name = 'vsoxseg2ei16.v'

    def golden(self):
        vl = self['vs2'].size
        vd_size = vl * self['nfields']
        vd = np.zeros( vd_size, dtype=self['vs3'].dtype )
        for no in range( 0, self['vs2'].size ):
            for idx in range( 0, self['nfields']):
                vd[int( self['vs2'][no]/self['vs3'].itemsize + idx)] = self['vs3'][ no*self['nfields']+idx]

        if 'v0' in self:
            mask = []
            for no in range(0, int(self['vs3'].size/self['nfields'])):
                mask = ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1
                if mask != 1:
                    for idx in range( 0, self['nfields'] ):
                        vd[ int( self['vs2'][no]/self['vs3'].itemsize + idx) ] = 0
            return vd
        else:
            return vd
