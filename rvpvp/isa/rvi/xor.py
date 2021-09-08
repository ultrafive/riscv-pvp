from ...isa.inst import *

class Xor(Inst):
    name = 'xor'

    def golden(self):
            return self['rs1'] ^ self['rs2']
