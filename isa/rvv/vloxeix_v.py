from isa.inst import *
import numpy as np
import math

class Vloxeix_v(Inst):
    name = 'vloxeix.v'

    def golden(self):

        vd = np.zeros( self['vl'], dtype=self['rs1'].dtype )
        for no in range( 0, self['vl'] ):
            vd[no] = self['rs1'][int( self['vs2'][no]/self['rs1'].itemsize )]

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vloxei8_v(Vloxeix_v):
    name = 'vloxei8.v'


class Vloxei16_v(Vloxeix_v):
    name = 'vloxei16.v'


class Vloxei32_v(Vloxeix_v):
    name = 'vloxei32.v'


class Vloxei64_v(Vloxeix_v):
    name = 'vloxei64.v'
                      
