from isa.inst import *
import numpy as np
import math

class Vsoxeix_v(Inst):
    name = 'vsoxeix.v'

    def golden(self):

        vd = np.zeros( self['rs1'].size, dtype=self['rs1'].dtype )
        if 'mask' not in self:
            for no in range( 0, self['vl'] ):
                vd[int( self['vs2'][no]/self['rs1'].itemsize )] = self['rs1'][no]
        else:
            mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
            for no in range( 0, self['vl'] ):
                if mask[no] != 0:
                    vd[int( self['vs2'][no]/self['rs1'].itemsize )] = self['rs1'][no]

        return vd

class Vsoxei8_v(Vsoxeix_v):
    name = 'vsoxei8.v'



class Vsoxei16_v(Vsoxeix_v):
    name = 'vsoxei16.v'



class Vsoxei32_v(Vsoxeix_v):
    name = 'vsoxei32.v'



class Vsoxei64_v(Vsoxeix_v):
    name = 'vsoxei64.v'


