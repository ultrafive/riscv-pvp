from isa.inst import *
import numpy as np

class Vmv_v_x(Inst):
    name = 'vmv.v.x'

    def golden(self):
        if self['ebits'] == 32:
            return np.array(self['rs1']).astype(np.int32)
        elif self['ebits'] == 16:
            return np.array(self['rs1']).astype(np.int16)
        elif self['ebits'] == 8:
            return np.array(self['rs1']).astype(np.int8)
        else:
            return np.array(self['rs1']).astype(np.int64)