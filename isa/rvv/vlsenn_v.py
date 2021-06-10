
from isa.inst import *
import numpy as np
import math

class _Vlsenn_v(Inst):
    sew = 0

    def golden(self):
        if self['rs2'] == 0:
            vd= np.full([self['vlen']], self['vs1'][0])
        else:
            self['rs2'] = np.asarray(self['rs2'], dtype=np.int32)
            vd = self['vs1'][::int(self['rs2']/self.sew)]
            vd = vd[:self['vlen']]

        return self.masked(vd)

class Vlse8_v(_Vlsenn_v):
    name = 'vlse8.v'
    sew = 1

class Vlse16_v(_Vlsenn_v):
    name = 'vlse16.v'
    sew = 2

class Vlse32_v(_Vlsenn_v):
    name = 'vlse32.v'
    sew = 4

class Vlse64_v(_Vlsenn_v):
    name = 'vlse64.v'
    sew = 8
