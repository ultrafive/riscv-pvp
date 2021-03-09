from isa.inst import *

class Vesub_mm(Inst):
    name = 'vesub.mm'

    def golden(self):
        if 'rs1' in self.keys():
            return self['rs1'] - self['rs2']