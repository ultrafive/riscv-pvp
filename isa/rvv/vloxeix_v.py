from isa.inst import *
import numpy as np
import math

class Vloxeix_v(Inst):
    name = 'vluxeix.v'

    def golden(self):

        vd = np.zeros( self['rs1'].size, dtype=self['rs1'].dtype )
        for no in range( 0, self['vs2'].size ):
            vd[no] = self['rs1'][int( self['vs2'][no]/self['rs1'].itemsize )]

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vloxei8_v(Vloxeix_v):
    name = 'vluxei8.v'


class Vloxei16_v(Vloxeix_v):
    name = 'vluxei16.v'


class Vloxei32_v(Vloxeix_v):
    name = 'vluxei32.v'


class Vloxei64_v(Vloxeix_v):
    name = 'vluxei64.v'
                      
