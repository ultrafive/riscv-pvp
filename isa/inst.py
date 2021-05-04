
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