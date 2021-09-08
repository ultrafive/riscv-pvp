from ...isa.inst import *

class Div(Inst):
    name = 'div'

    def golden(self):
        if self['rs2'] == 0:
            return -1
        else:
            return int( self['rs1'] / self['rs2'] )