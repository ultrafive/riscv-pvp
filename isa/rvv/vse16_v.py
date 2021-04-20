from isa.inst import *
import numpy as np
import math

class Vse16_v(Inst):
    name = 'vse16.v'

    def golden(self):
        if 'mask' not in self:
            return self['rs1']
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

            return np.ma.array(self['rs1'], mask = mask_list[0: self['vlen']], fill_value = 0).filled()
