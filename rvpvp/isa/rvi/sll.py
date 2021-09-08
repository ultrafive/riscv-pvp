from ...isa.inst import *
import numpy as np

class Sll(Inst):
    name = 'sll'

    def golden(self):
        rd = self['rs1'] << ( self['rs2'] & 0x1F )
        return ( rd & 0xffffffffffffffff )
