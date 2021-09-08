from ...isa.inst import *

class Mulhu(Inst):
    name = 'mulhu'

    def golden(self):
        return ( self['rs1'] * self['rs2'] ) >> 32