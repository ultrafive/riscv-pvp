from isa.inst import *
import numpy as np

class Vmv_x_s(Inst):
    name = 'vmv.x.s'

    def golden(self):
        return np.array(self['vs2'][0]).astype(np.int8)

class Vmv_x_s_16(Inst):
    name = 'vmv.x.s'

    def golden(self):
        return np.array(self['vs2'][0]).astype(np.int16)

class Vmv_x_s_32(Inst):
    name = 'vmv.x.s'

    def golden(self):
        return np.array(self['vs2'][0]).astype(np.int32)

class Vmv_x_s_64(Inst):
    name = 'vmv.x.s'

    def golden(self):
        return np.array(self['vs2'][0]).astype(np.int64)