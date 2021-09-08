from ...isa.inst import *
import ctypes
class Mulhsu(Inst):
    name = 'mulhsu'

    def golden(self):
        rs1 = ctypes.c_int32(self['rs1']).value
        rs2 = self['rs2']
        return ( rs1 * rs2 ) >> 32