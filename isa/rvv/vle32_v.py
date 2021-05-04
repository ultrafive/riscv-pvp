from isa.inst import *
import numpy as np
import math

class Vle32_v(Inst):
    name = 'vle32.v'

    def golden(self):
        if 'mask' not in self:
            return self['rs1']
        else:
            return np.where( self.mask() == 1, self['rs1'], 0)
