from ...isa.inst import *

class Sub(Inst):
    name = 'sub'

    def golden(self):
        rd = self['rs1'] - self['rs2']
        rd = rd & 0xffffffffffffffff
        return rd
