from ...isa.inst import *
import numpy as np
import math

class Vpopc_m(Inst):
    name = 'vpopc.m'

    def golden(self):
        if 'mask' in self:
            if 'vs2' not in self:
                tmp = np.unpackbits(self['mask'] & self['mask'], bitorder='little')[0: self['vl']]
            else:
                tmp = np.unpackbits(self['vs2'] & self['mask'], bitorder='little')[0: self['vl']]
        else:
            tmp = np.unpackbits(self['vs2'], bitorder='little')[0: self['vl']]
        return np.array([np.sum(tmp)])

class Vfirst_m(Inst):
    name = 'vfirst.m'

    def golden(self):
        if 'mask' in self:
            if 'vs2' not in self:
                tmp = np.unpackbits(self['mask'] & self['mask'], bitorder='little')[0: self['vl']]
            else:
                tmp = np.unpackbits(self['vs2'] & self['mask'], bitorder='little')[0: self['vl']]
        else:
            tmp = np.unpackbits(self['vs2'], bitorder='little')[0: self['vl']]
        firstOne = np.where(tmp==1)
        if np.size(firstOne) > 0:
          return np.array(np.min(firstOne))
        else:
          return np.array([-1], dtype=int)
