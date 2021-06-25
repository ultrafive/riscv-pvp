from isa.inst import *
import numpy as np
import math

class _Vsenn_v(Inst):
    def golden(self):
        return self.masked(self['rs1'])

class Vse1_v(_Vsenn_v):
    name = 'vse1.v'
    def golden( self ):
        return self['rs1']    
class Vse8_v(_Vsenn_v):
    name = 'vse8.v'

class Vse16_v(_Vsenn_v):
    name = 'vse16.v'

class Vse32_v(_Vsenn_v):
    name = 'vse32.v'

class Vse64_v(_Vsenn_v):
    name = 'vse64.v'

class Vse1_v(Inst):
    name = 'vse1.v'
    def golden(self):
        newLen = math.ceil(self['vlen']/8) * 8
        if 'mask' not in self:
            return np.packbits(np.unpackbits(self['rs1'], bitorder='little')[0: newLen], bitorder='little')
        else:
            tmp = np.unpackbits(self['rs1'] & self['mask'], bitorder='little')[0: newLen]
            return np.packbits(tmp, bitorder='little')
