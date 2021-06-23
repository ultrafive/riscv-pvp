from isa.inst import *
import numpy as np
import math

class Vsuxsegxeix_v(Inst):
    name = 'vsuxsegxeix.v'

    def golden(self):
        vd = np.zeros( self['vs3'].size, dtype=self['vs3'].dtype )
        for no in range(0, self['vlen']):
            start = int(self['idx'][no]/self['vs3'].itemsize)
            if 'mask' not in self:
                for idx in range(0, self['nfields']):
                    vd[start+idx] = self['vs3'][int(no*self['nfields']+idx)]
            else :
                mask_arr = np.unpackbits(self['mask'], bitorder='little')[0: self['vlen']]
                mask_bit = mask_arr[no]
                if mask_bit == 1:
                    for idx in range(0, self['nfields']):
                        vd[start+idx] = self['vs3'][int(no*self['nfields']+idx)]
        
        return vd
