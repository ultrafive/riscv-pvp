from isa.inst import *
import numpy as np
import math

class Vlsegxexff_v(Inst):
    name = 'vlsegXeXff.v'

    def golden(self):
        res = np.linspace(1, 0x400, 0x400, dtype=np.uint8)
        if self['ebits'] == 16:
            res.dtype = np.uint16
        elif self['ebits'] == 32:
            res.dtype = np.uint32
        elif self['ebits'] == 64:
            res.dtype = np.uint64
            
        if 'nvl' not in self:
            res = res[0:self['vlen']*self['nf']]
            return self.masked(res)
        else:
            return res[0-self['nvl']*self['nf']-1:-1]


                       