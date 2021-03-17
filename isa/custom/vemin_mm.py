from isa.inst import *
import numpy as np
class Vemin_mm(Inst):
    name = 'vemin.mm'

    def golden(self):
        if 'rs1' in self.keys():
            return np.minimum( self['rs1'], self['rs2'] )