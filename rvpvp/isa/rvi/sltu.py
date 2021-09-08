from ...isa.inst import *

class Sltu(Inst):
    name = 'sltu'

    def golden(self):

        if self['rs1'] < self['rs2']:
            rd = 1
        else:
            rd = 0
        if self['rs1'] == 0 and self['rs2'] != 0:
            rd = 1

        if self['rs1'] == 0 and self['rs2'] == 0:
            rd = 0

        if self['rs1'] != 0 and self['rs2'] == 0:
            rd = 0   

        return rd
