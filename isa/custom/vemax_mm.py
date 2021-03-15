from isa.inst import *
import numpy as np
class Vemax_mm(Inst):
    name = 'vemax.mm'

    def golden(self):
        if 'rs1' in self.keys():
            return np.maximum( self['rs1'], self['rs2'] )