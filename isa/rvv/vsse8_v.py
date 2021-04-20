from isa.inst import *
import numpy as np
import math

class Vsse8_v(Inst):
    name = 'vsse8.v'

    def golden(self):
        sew = 1
        zero_size = self['vlen'] * self['rs2'] + 1
        res=np.zeros(zero_size, np.int8)

        if 'mask' not in self and 'rs3' in self:
            for i, v in enumerate(self['rs3']):
                if i > self['vlen']:
                    break
                res[i * int(self['rs2']/sew)] = v
        elif 'mask' in self:
            mask_list = []
            for index in range(0, math.ceil(self['vlen'] / 8 )):
                v0_mask = self['mask'][index]
                for shift in range(0, 8):
                    mask_list.append(v0_mask & 1 == 0)
                    v0_mask = v0_mask >> 1

            for i, v in enumerate(self['rs3']):
                if i >= self['vlen']:
                    break

                if mask_list[i] == False:
                    res[i * int(self['rs2']/sew)] = v

        return res