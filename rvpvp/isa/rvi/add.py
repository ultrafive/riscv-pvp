from ...isa.inst import *

class Add(Inst):
    name = 'add'

    def golden(self):
        rd = self['rs1'] + self['rs2']
        rd = rd & 0xffffffffffffffff
        return rd
