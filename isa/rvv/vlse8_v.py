
from isa.inst import *
import numpy as np
import math

class Vlse8_v(Inst):
    name = 'vlse8.v'

    def golden(self):
        sew = 1

        if self['rs2'] == 0:
            vd= np.full([self['vlen']], self['rs1'][0])
        else:
            vd = self['rs1'][::int(self['rs2']/sew)]
            vd = vd[:self['vlen']]

        if 'mask' not in self:
            return vd
        else:
            mask_list = []
            for index in range(0, math.ceil(self['vlen'] / 8 )):
                v0_mask = self['mask'][index]
                for shift in range(0, 8):
                    if v0_mask & 1 == 0:
                        mask_list.append(True)
                    else:
                        mask_list.append(False)
                    v0_mask = v0_mask >> 1


            return np.ma.array(vd, mask = mask_list[0: self['vlen']], fill_value = 0).filled()

