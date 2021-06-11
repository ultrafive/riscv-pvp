from isa.inst import *
import numpy as np
import math

class Viota_m(Inst):
    name = 'viota.m'

    def golden(self):
        tmp = np.unpackbits(self['vs2'], bitorder='little')[0: self['vlen']]
        res = np.zeros(self['vlen']).astype('uint'+str(self['ebits']))
        for i in range(1, self['vlen']):
            res[i] = np.sum(tmp[0: i])
        return res