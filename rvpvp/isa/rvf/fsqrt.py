from ...isa.inst import *
import numpy as np

class Fsqrt(Inst):
    name = 'fsqrt.s'

    def golden(self):

        rs1 = np.array([self['rs1']]).astype(np.float32)

        rd = np.sqrt( rs1 )

        if np.isnan( rd ):
            return 0x7fc00000
        else:
            return rd[0]
       
