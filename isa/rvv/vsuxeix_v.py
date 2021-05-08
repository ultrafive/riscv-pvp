from isa.inst import *
import numpy as np
import math

class Vsuxeix_v(Inst):
    name = 'vsoxeix.v'

    def golden(self):

        vd = np.zeros( self['vs2'].size, dtype=self['vs3'].dtype )
        for no in range( 0, self['vs2'].size ):
            vd[int( self['vs2'][no]/self['vs3'].itemsize )] = self['vs3'][no]

        return self.masked( vd, self['rs1'] )

class Vsuxei8_v(Vsuxeix_v):
    name = 'vsoxei8.v'



class Vsuxei16_v(Vsuxeix_v):
    name = 'vsoxei16.v'



class Vsuxei32_v(Vsuxeix_v):
    name = 'vsoxei32.v'



class Vsuxei64_v(Vsuxeix_v):
    name = 'vsoxei64.v'


