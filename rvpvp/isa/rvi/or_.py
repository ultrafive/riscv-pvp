from ...isa.inst import *

class Or(Inst):
    name = 'or'

    def golden(self):
            return self['rs1'] | self['rs2']
