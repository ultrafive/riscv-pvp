from ...isa.inst import *
import numpy as np

class Fnmsub(Inst):
    name = 'fnmsub.s'

    def golden(self):
        return -self['rs1']*self['rs2']+self['rs3']
       
