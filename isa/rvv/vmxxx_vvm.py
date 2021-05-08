from isa.inst import *
import numpy as np
import math

class Vmadc_vvm(Inst):
    name = 'vmadc.vvm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vlen']]
        vd = self['vs2'].astype(np.int64) + self['vs1'] + mask
        vd=np.where(vd > 0xffffffff, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vlen']]

class Vmsbc_vvm(Inst):
    name = 'vmsbc.vvm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vlen']]
        vd = self['vs2'].astype(np.int64) - self['vs1'] - mask
        vd=np.where(vd < 0, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vlen']]