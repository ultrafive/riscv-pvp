from isa.inst import *
import numpy as np

class Vfwsub_vv(Inst):
    name = 'vfwsub.vv'

    def golden(self):
        dtype_vs = self['rs1'].dtype
        if dtype_vs == np.float16:
            dtype_vd = np.float32
        elif dtype_vs == np.float32:
            dtype_vd = np.float64
        if 'v0' in self:
            mask = []
            for no in range(0, self['rs1'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, self['rs2'].astype( dtype_vd ) - self['rs1'].astype( dtype_vd ), self['orig'])
        else:
            return self['rs2'].astype( dtype_vd ) - self['rs1'].astype( dtype_vd )
