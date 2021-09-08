from ...isa.inst import *
import ctypes 

class Slt(Inst):
    name = 'slt'

    def golden(self):
        rs1 = ctypes.c_int64( self['rs1'] ).value
        rs2 = ctypes.c_int64( self['rs2'] ).value

        if rs1 < rs2:
            return 1
        else:
            return 0
