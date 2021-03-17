from isa.inst import *
import numpy as np
class Velut_m(Inst):
    name = 'velut.m'

    def golden( self ):
        if 'rs1' in self.keys():
            return self['rs2'][list(map(lambda x: int(x.byteswap().tobytes().hex(), 16), self['rs1'].flatten()))].reshape(self['rs1'].shape).astype(np.half)