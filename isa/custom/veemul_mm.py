from isa.inst import *

class Veemul_mm(Inst):
    name = 'veemul.mm'

    def golden(self):
        if 'rs1' in self.keys():
            return self['rs1'] * self['rs2']