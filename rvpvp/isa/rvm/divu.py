from ...isa.inst import *
import ctypes
class Divu(Inst):
    name = 'divu'

    def golden(self):
        rs1 = ctypes.c_uint32( self['rs1'] ).value
        rs2 = ctypes.c_uint32( self['rs2'] ).value
        if rs2 == 0:
            return -1
        else:
            return int( rs1 / rs2 )