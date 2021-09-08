from ...isa.inst import *
import ctypes
class Remu(Inst):
    name = 'remu'

    def golden(self):
        rs1 = ctypes.c_uint32( self['rs1'] ).value
        rs2 = ctypes.c_uint32( self['rs2'] ).value
        if rs2 == 0:
            return rs1
        else:
            d = int( rs1 / rs2 )
            return rs1 - d * rs2