from ...isa.inst import *
import numpy as np

class Slli(Inst):
    name = 'slli'

    def golden(self):
        rd = self['rs1'] << ( self['imm'] & 0x1F )
        return ( rd & 0xffffffffffffffff )
