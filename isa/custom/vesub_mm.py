from isa.inst import *

class Vesub_mm(Inst):
    name = 'vesub.mm'

    def golden(self):
        return self['rs1'] - self['rs2']