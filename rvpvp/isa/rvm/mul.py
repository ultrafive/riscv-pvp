from ...isa.inst import *

class Mul(Inst):
    name = 'mul'

    def golden(self):
        return ( self['rs1'] * self['rs2'] ) & 0xFFFFFFFF