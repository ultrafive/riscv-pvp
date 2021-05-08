from isa.inst import *
import numpy as np

class Vmv_v_i(Inst):
    name = 'vmv.v.i'

    def golden(self):
        if self['ebits'] == 32:
            return np.array(self['imm']).astype(np.int32)
        elif self['ebits'] == 16:
            return np.array(self['imm']).astype(np.int16)
        elif self['ebits'] == 8:
            return np.array(self['imm']).astype(np.int8)
        else:
            return np.array(self['imm']).astype(np.int64)