from isa.inst import *
import numpy as np
import math

class Vluxei8_v(Inst):
    name = 'vluxei8.v'

    def golden(self):
        sew = 1

        if 'mask' not in self:
            vd = np.linspace(0,0,self['vlen'], dtype=self['rs1'].dtype)
            for x in range(self['vlen']):
                vd[x] = self['rs1'][int(self['rs2'][x]/sew)]
            return vd
        else:
            vd = np.linspace(0,0,self['vlen'], dtype=self['rs1'].dtype)

            for index in range(0, math.ceil(self['vlen'] / 8 )):
                v0_mask = self['mask'][index]
                for shift in range(0, 8):
                    if v0_mask & 1 == 0:
                       vd[x] = self['rs1'][int(self['rs2'][x]/sew)]

                    v0_mask = v0_mask >> 1
            return vd
