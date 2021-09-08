from ...isa.inst import *
import numpy as np

class Fadd(Inst):
    name = 'fadd.s'

    def golden(self):

        rs1 = np.array([self['rs1']]).astype(np.float32)
        rs2 = np.array([self['rs2']]).astype(np.float32)

        rd = rs1 + rs2

        return rd[0]
       
