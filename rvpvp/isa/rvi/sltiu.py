from ...isa.inst import *
import ctypes 

class Sltiu(Inst):
    name = 'sltiu'

    def golden(self):
        if self['imm'] & 0x800 == 0x800:
            imm = self['imm'] + 0xfffffffffffff000
        else:
            imm = self['imm']
        rs1 = self['rs1']

        if rs1 < imm:
            rd = 1
        else:
            rd = 0

        if rs1 == 0 and imm == 1:
            rd = 1
        if rs1 != 0 and imm == 1:
            rd = 0
        
        return rd
