from isa.inst import *

class Addi(Inst):
    name = 'addi'

    def golden(self):
        return self['rs1'] + self['imm']