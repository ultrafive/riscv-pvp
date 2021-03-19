from isa.inst import *

class Veadd_mm(Inst):
    name = 'veadd.mm'

    def golden(self):
        if 'rs1' in self.keys():
            return self['rs1'] + self['rs2']