from ...isa.inst import *

class And(Inst):
    name = 'and'

    def golden(self):
            return self['rs1'] & self['rs2']
