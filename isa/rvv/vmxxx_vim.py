from isa.inst import *
import numpy as np

class Vmadc_vim(Inst):
    name = 'vmadc.vim'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vl']]
        vd = self['vs2'].astype(np.uint64) + self['imm'] + mask
        vd = np.where(vd > 0xffffffff, 1, 0)
        return np.packbits(vd, bitorder='little')[0: self['vl']]