from isa.inst import *
import numpy as np
import math

class Vsuxeix_v(Inst):
    name = 'vluxeix.v'

    def golden(self):

        vd = np.zeros( self['rs1'].size, dtype=self['rs1'].dtype )
        if 'mask' not in self:
            for no in range( 0, self['vlen'] ):
                vd[int( self['vs2'][no]/self['rs1'].itemsize )] = self['rs1'][no]
        else:
            mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vlen']]
            for no in range( 0, self['vlen'] ):
                if mask[no] != 0:
                    vd[int( self['vs2'][no]/self['rs1'].itemsize )] = self['rs1'][no]

        return vd

class Vsuxei8_v(Vsuxeix_v):
    name = 'vsuxei8.v'

class Vsuxei16_v(Vsuxeix_v):
    name = 'vsuxei16.v'



class Vsuxei32_v(Vsuxeix_v):
    name = 'vsuxei32.v'



class Vsuxei64_v(Vsuxeix_v):
    name = 'vsuxei64.v'


