from isa.inst import *
import numpy as np

class Vecvt_hf_xu8_m(Inst):
    name = 'vecvt.hf.xu8.m'

    def golden( self ):
        if 'rs1' in self.keys():
            return self['rs1'].astype( np.half )