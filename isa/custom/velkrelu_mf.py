from isa.inst import *
import numpy as np

class Velkrelu_mf(Inst):
    name = 'velkrelu.mf'

    def golden(self):
        if 'rs1' in self.keys():
            rd = np.where( self['rs1'] <= 0, self['rs1'] * self['rs2'], self['rs1'] ).astype( np.float16 )
            return rd

