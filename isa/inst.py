
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