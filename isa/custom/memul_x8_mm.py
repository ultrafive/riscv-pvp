from isa.inst import *
import numpy as np

class Memul_x8_mm(Inst):
    name = 'memul.x8.mm'

    def golden( self ):
        if 'vs1' in self.keys():
            return np.matmul( self['vs1'], self['vs2'], dtype=np.int32 )