from ...isa.inst import *
import numpy as np

class Srl(Inst):
    name = 'srl'

    def golden(self):
        rd = ( self['rs1'] & 0xFFFFFFFF ) >> ( self['rs2'] & 0x1F )
        return rd
