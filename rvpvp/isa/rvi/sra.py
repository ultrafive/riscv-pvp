from ...isa.inst import *
import numpy as np

class Sra(Inst):
    name = 'sra'

    def golden(self):
        rs2 = self['rs2'] & 0x1F 
        rd =  self['rs1'] >> rs2
        if ( self[ 'rs1'] >> 63 ) == 1:
            rd = rd +  ( ( ( 1 << rs2 ) - 1 ) << ( 64 - rs2 ) )
        return rd
