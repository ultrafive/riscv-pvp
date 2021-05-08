from isa.inst import *
import numpy as np
import math

class Vlsegxex_v(Inst):
    name = 'vlsegxex.v'

    def golden(self):

        vd = self['rs1'].copy()

        if 'mask' in self:
            mask = []
            for no in range(0, int(self['rs1'].size/self['nfields'])):
                mask = ( self['mask'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1
                if mask != 1:
                    for idx in range( 0, self['nfields'] ):
                        vd[ int(self['nfields']*no+idx) ] = self['orig'][int(self['nfields']*no+idx)]
            return vd
        else:
            return vd
