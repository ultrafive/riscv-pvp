from isa.inst import *

class Veadd_mm(Inst):
    name = 'veadd.mm'

    def golden(self):
        return self['rs1'] + self['rs2']