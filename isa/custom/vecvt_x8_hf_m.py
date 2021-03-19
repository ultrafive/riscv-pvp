from isa.inst import *
import numpy as np

class Vecvt_x8_hf_m(Inst):
    name = 'vecvt.x8.hf.m'

    def golden( self ):
        if 'rs1' in self.keys():
            rd = np.where(self['rs1'] < -128, -128, self['rs1'])
            rd = np.where(rd > 127, 127, rd )
            return rd.astype( np.int8 )