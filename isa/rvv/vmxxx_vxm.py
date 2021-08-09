from isa.inst import *
import numpy as np
import math

class Vmadc_vxm(Inst):
    name = 'vmadc.vxm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vl']]
        vd = self['vs2'].astype(np.uint64) + self['rs1'] + mask
        vd=np.where(vd > 0xffffffff, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vl']]

class Vmsbc_vxm(Inst):
    name = 'vmsbc.vxm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vl']]
        vd = self['vs2'].astype(np.int64) - self['rs1'] - mask
        vd=np.where(vd < 0, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vl']]