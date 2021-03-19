from isa.inst import *
import numpy as np

class Velkrelu_mv(Inst):
    name = 'velkrelu.mv'

    def golden(self):
        if 'rs1' in self.keys():
            rd = np.where( self['rs1'] <= 0, self['rs1'] * self['rs2'], self['rs1'] ).astype( np.float16 )
            rd = np.where( self['rs1'] == 0, self['rs1'], rd ).astype( np.float16 )
            return rd

