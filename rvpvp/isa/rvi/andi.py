from ...isa.inst import *

class Andi(Inst):
    name = 'andi'

    def golden(self):
        if self['imm'] & 0x800 == 0x800:
            imm = self['imm'] + 0xfffffffffffff000
            rd = self['rs1'] & imm
        else:
            rd = self['rs1'] & self['imm']

        return rd
