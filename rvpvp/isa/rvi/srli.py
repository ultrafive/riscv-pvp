from ...isa.inst import *
import numpy as np

class Srli(Inst):
    name = 'srli'

    def golden(self):
        rd = ( self['rs1'] & 0xFFFFFFFF ) >> ( self['imm'] & 0x1F )
        return rd
