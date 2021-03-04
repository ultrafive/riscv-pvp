from isa.inst import *

class Ori(Inst):
    name = 'ori'

    def golden(self):
        return self['rs1'] | self['imm']