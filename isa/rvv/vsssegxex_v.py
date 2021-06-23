from isa.inst import *
import numpy as np
import math

class Vsssegxex_v(Inst):
    name = 'vsssegxex.v'

    def golden(self):

        vl = self['vlen']
        vd_size = (self['vlen'] - 1) * self['rs2'] + self['nfields']
        stride = self['rs2']/self['vs3'].itemsize
        vd = np.zeros( int(vd_size), dtype=self['vs3'].dtype )
        for no in range( 0, int(vl)):
            for idx in range( 0, self['nfields']):
                vd[ int(no*stride+idx) ] = self['vs3'][int(no*self['nfields']+idx)]


        if 'mask' in self:
            mask = []
            for no in range(0, vl):
                mask = ( self['mask'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1
                if mask != 1:
                    for idx in range( 0, self['nfields'] ):
                        vd[ int(no*stride+idx) ] = 0
            return vd
        else:
            return vd
