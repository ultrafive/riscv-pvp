from isa.inst import *
import numpy as np
import math

class Vid_v(Inst):
    name = 'vid.v'

    def golden(self):
        res = np.arange(self['vl']).astype('uint'+str(self['ebits']))
        if 'mask' in self:
            mask = np.unpackbits(self['mask'], bitorder='little')[0:self['vl']]
            res = np.where(mask==1, res, 0)
        return res