from ...isa.inst import *
import ctypes 

class Slti(Inst):
    name = 'slti'

    def golden(self):
        if self['imm'] & 0x800 == 0x800:
            imm = self['imm'] + 0xfffffffffffff000
        else:
            imm = self['imm']
        imm = ctypes.c_int64( imm ).value
        rs1 = ctypes.c_int64( self['rs1'] ).value

        if rs1 < imm:
            return 1
        else:
            return 0
