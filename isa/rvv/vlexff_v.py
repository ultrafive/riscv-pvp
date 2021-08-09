from isa.inst import *
import numpy as np
import math

class Vlexff_v(Inst):
    name = 'vlexff.v'

    def golden(self):
        res = np.linspace(1, 0x400, 0x400, dtype=np.uint8)
        if self['ebits'] == 16:
            res.dtype = np.uint16
        elif self['ebits'] == 32:
            res.dtype = np.uint32
        elif self['ebits'] == 64:
            res.dtype = np.uint64
            
        if 'nvl' not in self:
            res = res[0:self['vl']]
            return self.masked(res)
        else:
            return res[0-self['nvl']-1:-1]

class Vle8ff_v(Vlexff_v):
    name = 'vle8ff.v'


class Vle16ff_v(Vlexff_v):
    name = 'vle16ff.v'


class Vle32ff_v(Vlexff_v):
    name = 'vle32ff.v'


class Vle64ff_v(Vlexff_v):
    name = 'vle64ff.v'

                       