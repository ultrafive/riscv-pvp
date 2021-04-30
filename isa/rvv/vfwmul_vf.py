from isa.inst import *
import numpy as np

class Vfwmul_vf(Inst):
    name = 'vfwmul.vf'

    def golden(self):
        dtype_vs = self['vs2'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, self['rs1'].astype( dtype_vd ) * self['vs2'].astype( dtype_vd ), self['orig'])
        else:
            return self['rs1'].astype( dtype_vd ) * self['vs2'].astype( dtype_vd )