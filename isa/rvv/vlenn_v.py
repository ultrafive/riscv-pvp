from isa.inst import *
import math

class _Vlenn_v(Inst):
    def golden(self):
        return self.masked(self['rs1'])

class Vle1_v(_Vlenn_v):
    name = 'vle1.v'

    def golden( self ):
        return self['rs1']
        
class Vle8_v(_Vlenn_v):
    name = 'vle8.v'

class Vle16_v(_Vlenn_v):
    name = 'vle16.v'

class Vle32_v(_Vlenn_v):
    name = 'vle32.v'

class Vle64_v(_Vlenn_v):
    name = 'vle64.v'

class Vle1_v(Inst):
    name = 'vle1.v'
    def golden(self):
        newLen = math.ceil(self['vlen']/8) * 8
        if 'mask' not in self:
            return np.packbits(np.unpackbits(self['rs1'], bitorder='little')[0: newLen], bitorder='little')
        else:
            tmp = np.unpackbits(self['rs1'] & self['mask'], bitorder='little')[0: newLen]
            return np.packbits(tmp, bitorder='little')

