from isa.inst import *
import numpy as np

class Vmv_s_x(Inst):
    name = 'vmv.s.x'

    def golden(self):
        if self['ebits'] == 32:
            return np.array(self['rs1']).astype(np.int32)
        elif self['ebits'] == 16:
            return np.array(self['rs1']).astype(np.int16)
        elif self['ebits'] == 8:
            return np.array(self['rs1']).astype(np.int8)
        else:
            return np.array(self['rs1']).astype(np.int64)

class Vmv_s_x_16(Inst):
    name = 'vmv.s.x'

    def golden(self):
        return np.array(self['rs1']).astype(np.int16)

class Vmv_s_x_32(Inst):
    name = 'vmv.s.x'

    def golden(self):
        return np.array(self['rs1']).astype(np.int32)