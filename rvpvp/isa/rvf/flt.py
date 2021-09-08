from ...isa.inst import *
import numpy as np

class Flt(Inst):
    name = 'flt.s'

    def golden(self):

        rs1 = np.array([self['rs1']]).astype(np.float32)
        rs2 = np.array([self['rs2']]).astype(np.float32)

        if rs1 < rs2:
            return 1
        else:
            return 0
       
