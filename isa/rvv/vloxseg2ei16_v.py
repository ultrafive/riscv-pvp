from isa.inst import *
import numpy as np
import math

class Vloxseg2ei16_v(Inst):
    name = 'vloxseg2ei16.v'

    def golden(self):
        vl = self['vs2'].size
        vd_size = vl * self['nfields']
        vd = np.zeros( vd_size, dtype=self['rs1'].dtype )
        for no in range( 0, self['vs2'].size ):
            for idx in range(0, int(self['nfields']) ):
                vd[int( no*self['nfields']+idx )] = self['rs1'][int( self['vs2'][no]/self['rs1'].itemsize +idx )]

        if 'v0' in self:
            mask = []
            for no in range( 0, vl ):
                mask = ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1
                if mask != 1:
                    for idx in range( 0, self['nfields'] ):
                        vd[ int(self['nfields']*no+idx) ] = self['orig'][int(self['nfields']*no+idx)]
            return vd
        else:
            return vd
