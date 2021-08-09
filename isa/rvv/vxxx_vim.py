from isa.inst import *
import numpy as np

class Vadc_vim(Inst):
    name = 'vadc.vim'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vl']]
        return self['vs2'] + self['imm'] + mask

class Vmerge_vim(Inst):
    name = 'vmerge.vim'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vl']]
        return np.where(mask & 1 == 1, np.array(self['imm']), self['vs2'])
