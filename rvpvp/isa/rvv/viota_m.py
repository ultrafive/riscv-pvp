from ...isa.inst import *
import numpy as np
import math

class Viota_m(Inst):
    name = 'viota.m'

    def golden(self):
        if self['ebits'] <= 64:
            if 'mask' in self:
                if 'vs2' in self:
                    tmp = np.unpackbits(self['vs2'] & self['mask'], bitorder='little')[0: self['vl']]
                else:
                    tmp = np.unpackbits(self['mask'] & self['mask'], bitorder='little')[0: self['vl']]
            else:
                tmp = np.unpackbits(self['vs2'], bitorder='little')[0: self['vl']]
            res = np.zeros(self['vl']).astype('uint'+str(self['ebits']))
            for i in range(1, self['vl']):
                res[i] = np.sum(tmp[0: i])
            
            if 'mask' in self:
                mask = np.unpackbits(self['mask'], bitorder='little')[0:self['vl']]
                res = np.where( mask == 1, res, 0)
            if 'orign' in self:
                orign_val = self['orign']
                if 'mask' in self:
                    mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
                    res = np.where( mask == 1, res, orign_val[0:self['vl']])
                orign_val[0:self['vl']] = res[0:self['vl']]
                return orign_val
        
            return res
