from isa.inst import *
import numpy as np

class Vadc_vvm(Inst):
    name = 'vadc.vvm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vlen']]
        return self['vs1'] + self['vs2'] + mask

class Vsbc_vvm(Inst):
    name = 'vsbc.vvm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vlen']]
        return self['vs2'] - self['vs1'] - mask

class Vmerge_vvm(Inst):
    name = 'vmerge.vvm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vlen']]
        return np.where(mask & 1 == 1, self['vs1'], self['vs2'])