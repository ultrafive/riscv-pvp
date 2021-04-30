from isa.inst import *
import numpy as np
import math

class Vssseg2e32_v(Inst):
    name = 'vssseg2e32.v'

    def golden(self):

        vl = self['vs3'].size/self['nfields']
        vd_size = vl * self['rs2']/self['vs3'].itemsize
        stride = self['rs2']/self['vs3'].itemsize
        vd = np.zeros( int(vd_size), dtype=self['vs3'].dtype )
        for no in range( 0, int(vl)):
            for idx in range( 0, self['nfields']):
                vd[ int(no*stride+idx) ] = self['vs3'][int(no*self['nfields']+idx)]


        if 'v0' in self:
            mask = []
            for no in range(0, int(self['vs3'].size/self['nfields'])):
                mask = ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1
                if mask != 1:
                    for idx in range( 0, self['nfields'] ):
                        vd[ int(no*stride+idx) ] = 0
            return vd
        else:
            return vd
