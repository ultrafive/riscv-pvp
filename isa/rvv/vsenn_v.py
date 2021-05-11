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
