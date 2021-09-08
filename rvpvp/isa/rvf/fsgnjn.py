from ...isa.inst import *

class Fsgnjn(Inst):
    name = 'fsgnjn.s'

    def golden(self):
        if 'rs2_sign' in self.keys():
            return 1-self['rs2_sign']
       
