from isa.inst import *
import numpy as np
import math

class Vsoxeix_v(Inst):
    name = 'vsoxeix.v'

    def golden(self):

        vd = np.zeros( self['vs2'].size, dtype=self['vs3'].dtype )
        for no in range( 0, self['vs2'].size ):
            vd[int( self['vs2'][no]/self['vs3'].itemsize )] = self['vs3'][no]

        return self.masked( vd, self['rs1'] )

class Vsoxei8_v(Vsoxeix_v):
    name = 'vsoxei8.v'



class Vsoxei16_v(Vsoxeix_v):
    name = 'vsoxei16.v'



class Vsoxei32_v(Vsoxeix_v):
    name = 'vsoxei32.v'



class Vsoxei64_v(Vsoxeix_v):
    name = 'vsoxei64.v'


