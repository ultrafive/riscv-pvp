from ...isa.inst import *
import numpy as np

class Fsgnjx(Inst):
    name = 'fsgnjx.s'

    def golden(self):
        if 'rs2_sign' in self.keys():
            return self['rs1_sign'] ^ self['rs2_sign']
       
