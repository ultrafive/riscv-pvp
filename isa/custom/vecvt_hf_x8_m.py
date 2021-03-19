from isa.inst import *
import numpy as np

class Vecvt_hf_x8_m(Inst):
    name = 'vecvt.hf.x8.m'

    def golden( self ):
        if 'rs1' in self.keys():
            return self['rs1'].astype( np.half )