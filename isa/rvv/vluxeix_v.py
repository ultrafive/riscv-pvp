from isa.inst import *
import numpy as np
import math

class Vluxeix_v(Inst):
    name = 'vluxeix.v'

    def golden(self):

        vd = np.zeros( self['vlen'], dtype=self['rs1'].dtype )
        for no in range( 0, self['vlen'] ):
            vd[no] = self['rs1'][int( self['vs2'][no]/self['rs1'].itemsize )]

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vluxei8_v(Vluxeix_v):
    name = 'vluxei8.v'


class Vluxei16_v(Vluxeix_v):
    name = 'vluxei16.v'


class Vluxei32_v(Vluxeix_v):
    name = 'vluxei32.v'


class Vluxei64_v(Vluxeix_v):
    name = 'vluxei64.v'
                      
