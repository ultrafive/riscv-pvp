from isa.inst import *
import math

class _Vlenn_v(Inst):
    def golden(self):
        return self.masked(self['rs1'])

class Vle8_v(_Vlenn_v):
    name = 'vle8.v'

class Vle16_v(_Vlenn_v):
    name = 'vle16.v'

class Vle32_v(_Vlenn_v):
    name = 'vle32.v'

class Vle64_v(_Vlenn_v):
    name = 'vle64.v'
