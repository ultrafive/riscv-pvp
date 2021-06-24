from isa.inst import *
import numpy as np
import math

class Viota_m(Inst):
    name = 'viota.m'

    def golden(self):
        if 'mask' in self:
            tmp = np.unpackbits(self['vs2'] & self['mask'], bitorder='little')[0: self['vlen']]
        else:
            tmp = np.unpackbits(self['vs2'], bitorder='little')[0: self['vlen']]
        res = np.zeros(self['vlen']).astype('uint'+str(self['ebits']))
        for i in range(1, self['vlen']):
            res[i] = np.sum(tmp[0: i])
        
        if 'mask' in self:
          mask = np.unpackbits(self['mask'], bitorder='little')[0:self['vlen']]
          res = np.where( mask == 1, res, 0)
        
        return res