from ...isa.inst import *

class Fsgnj(Inst):
    name = 'fsgnj.s'

    def golden(self):
        if 'rs2_sign' in self.keys():
            return self['rs2_sign']
       
