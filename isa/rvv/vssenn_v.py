from isa.inst import *
import numpy as np
import math

class _Vssenn_v(Inst):
    sew = 0
    dtype = np.int8

    def golden(self):
        zero_size = (self['vl'] - 1) * self['rs2'] + 1
        res = np.zeros(zero_size, self.dtype)

        if 'mask' in self:
            mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]

        for i, v in enumerate(self['vs3']):
            if i >= self['vl']:
                break
            if 'mask' in self and mask[i] == 0:
                continue
            res[i * int(self['rs2']/self.sew)] = v
        return res

class Vsse8_v(_Vssenn_v):
    name = 'vsse8.v'
    sew = 1
    dtype = np.int8

class Vsse16_v(_Vssenn_v):
    name = 'vsse16.v'
    sew = 2
    dtype = np.int16

class Vsse32_v(_Vssenn_v):
    name = 'vsse32.v'
    sew = 4
    dtype = np.int32

class Vsse64_v(_Vssenn_v):
    name = 'vsse64.v'
    sew = 8
    dtype = np.int64