from ...isa.inst import *
import ctypes
class Mulh(Inst):
    name = 'mulh'

    def golden(self):
        rs1 = ctypes.c_int32(self['rs1']).value
        rs2 = ctypes.c_int32(self['rs2']).value
        return ( rs1 * rs2 ) >> 32