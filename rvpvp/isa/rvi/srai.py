from ...isa.inst import *
import numpy as np

class Srai(Inst):
    name = 'srai'

    def golden(self):
        imm = self['imm'] & 0x1F 
        rd =  self['rs1'] >> imm
        if ( self[ 'rs1'] >> 63 ) == 1:
            rd = rd +  ( ( ( 1 << imm ) - 1 ) << ( 64 - imm ) )
        return rd
