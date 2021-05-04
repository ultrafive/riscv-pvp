from isa.inst import *
import numpy as np
import math

class Vle8_v(Inst):
    name = 'vle8.v'

    def golden(self):
        if 'mask' not in self:
            return self['rs1']
        else:
            return np.where( self.mask() == 1, self['rs1'], 0)
