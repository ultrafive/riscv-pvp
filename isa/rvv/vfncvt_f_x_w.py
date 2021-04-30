from isa.inst import *
import numpy as np
import math

class Vfncvt_f_x_w(Inst):
    name = 'vfncvt.f.x.w'

    def golden(self):

        if self['vs2'].dtype == np.int32:
            target_dtype = np.float16
        elif self['vs2'].dtype == np.int64:
            target_dtype = np.float32

        vd = self['vs2'].astype( target_dtype )

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd