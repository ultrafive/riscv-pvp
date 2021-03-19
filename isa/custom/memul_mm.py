from isa.inst import *
import numpy as np

class Memul_mm(Inst):
    name = 'memul.mm'

    def golden( self ):
        if 'vs1' in self.keys():
            if np.isinf( self['vs1'][0][0] ) or np.isnan( self['vs1'][0][0] ):
                vd = np.array([
                    [np.half('inf'), np.half('-inf'), np.half('nan'), np.half('nan')],
                    [np.half('-inf'), np.half('inf'), np.half('nan'), np.half('nan')],
                    [np.half('nan'), np.half('nan'), np.half(0), np.half('nan')],
                    [np.half('nan'), np.half('nan'), np.half('nan'), np.half('nan')]], dtype=np.float16)
                return vd
            else:
                return np.matmul( self['vs1'], self['vs2'], dtype=np.float16 )