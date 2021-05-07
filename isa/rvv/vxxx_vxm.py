from isa.inst import *
import numpy as np

class Vadc_vxm(Inst):
    name = 'vadc.vxm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vlen']]
        return self['vs2'] + self['rs1'] + mask

class Vsbc_vxm(Inst):
    name = 'vsbc.vxm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vlen']]
        return self['vs2'] - self['rs1'] - mask

class Vmerge_vxm(Inst):
    name = 'vmerge.vxm'

    def golden(self):
        mask = np.unpackbits(self['v0'], bitorder='little')[0: self['vlen']]
        return np.where(mask & 1 == 1, self['rs1'], self['vs2'])