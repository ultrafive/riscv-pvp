from isa.inst import *
import numpy as np
import math

class Vfcvt_f_xu_v(Inst):
    name = 'vfcvt.f.xu.v'

    def golden(self):

        if self['vs2'].dtype == np.uint16:
            target_dtype = np.float16
        elif self['vs2'].dtype == np.uint32:
            target_dtype = np.float32
        elif self['vs2'].dtype == np.uint64:
            target_dtype = np.float64

        vd = self['vs2'].astype( target_dtype )

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd