from isa.inst import *
import numpy as np

lmul = {'1': 1, '2': 2, '4': 4, '8': 8, 'f2': 1/2, 'f4': 1/4, 'f8': 1/8}

class Vrgather_vi(Inst):
    name = 'vrgather.vi'

    def golden(self):
        vd = np.zeros(self['vs2'].size, dtype = np.uint32)
        vlmax = int(lmul[str(self['lmul'])] * self['VLEN'] / self['ebits'])
        for i in range (0, self['vlen']):
            if self['imm'] >= vlmax:
                vd[i] = 0
            else:
                vd[i] = self['vs2'][self['imm']]

        return self.masked(vd)

class Vrgather_vx(Inst):
    name = 'vrgather.vx'

    def golden(self):
        vd = np.zeros(self['vs2'].size, dtype = np.uint32)
        vlmax = int(lmul[str(self['lmul'])] * self['VLEN'] / self['ebits'])
        for i in range (0, self['vlen']):
            if self['rs1'] >= vlmax:
                vd[i] = 0
            else:
                vd[i] = self['vs2'][self['rs1']]

        return self.masked(vd)

class Vrgather_vv(Inst):
    name = 'vrgather.vv'

    def golden(self):
        vd = np.zeros(self['vs1'].size, dtype = np.uint32)
        vlmax = int(lmul[str(self['lmul'])] * self['VLEN'] / self['ebits'])
        for i in range (0, self['vlen']):
            if self['vs1'][i] >= vlmax:
                vd[i] = 0
            else:
                vd[i] = self['vs2'][self['vs1'][i]]

        return self.masked(vd)