from isa.inst import *
import numpy as np
import math

class Vloxsegxeix_v(Inst):
    name = 'vloxsegxeix.v'

    def golden(self):
        vl = self['vs2'].size
        vd_size = vl * self['nfields']
        vd = np.zeros( vd_size, dtype=self['rs1'].dtype )
        for no in range( 0, self['vs2'].size ):
            for idx in range(0, int(self['nfields']) ):
                vd[int( no*self['nfields']+idx )] = self['rs1'][int( self['vs2'][no]/self['rs1'].itemsize +idx )]

        if 'mask' in self:
            mask = []
            for no in range( 0, vl ):
                mask = ( self['mask'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1
                if mask != 1:
                    for idx in range( 0, self['nfields'] ):
                        vd[ int(self['nfields']*no+idx) ] = self['orig'][int(self['nfields']*no+idx)]
            return vd
        else:
            return vd
