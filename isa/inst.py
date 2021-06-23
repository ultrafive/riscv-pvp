
import sys
import numpy as np

class Inst(dict):
    name = 'unknown'

    def golden(self):
        raise NotImplementedError()

    def masked(self, value, old = 0):
        if 'mask' not in self:
            return value
        else:
            mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vlen']]
            return np.where( mask == 1, value, old)

    def as_mask(self, value):
        return np.packbits(np.unpackbits(value, bitorder='little')[0: self['vlen']], bitorder='little')


    def where(self):
        if 'mask' not in self:
            return True
        else:
            return np.unpackbits(self['mask'], bitorder='little')[0: self['vlen']] == 1
    
    def rounding(self, value):
        if self['mode'] == 0:
            res = value + 1
        elif self['mode'] == 1:
            res = np.where(value%4==3, value+1, value)
        elif self['mode'] == 2:
            res = value
        elif self['mode'] == 3:
            res = np.where(value%4==1, value+2, value)

        return res

