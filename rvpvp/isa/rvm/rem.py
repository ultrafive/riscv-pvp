from ...isa.inst import *

class Rem(Inst):
    name = 'rem'

    def golden(self):
        if self['rs2'] == 0:
            return self['rs1']
        else:
            d = int( self['rs1'] / self['rs2'] )
            return self['rs1'] - d * self['rs2']