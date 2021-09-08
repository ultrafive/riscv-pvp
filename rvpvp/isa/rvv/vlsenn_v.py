from ...isa.inst import *
import numpy as np
import math

factor_lmul = { 1:1, 2:2, 4:4, 8:8, 'f2':0.5, 'f4':0.25, 'f8':0.125}

class Vlsex_v(Inst):
    name = 'vlsex.v'

    def golden(self):
        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(self['vl'], dtype=self['rs1'].dtype)
        vl = self['vl']
        emul = self['eew'] /self['sew']*factor_lmul[self['lmul']]
        emul = 1 if emul < 1 else int(emul)
        vlmax = int(emul * self['VLEN'] // (self['rs1'].itemsize*8))

        rs1 = self['rs1']
        eew = self['eew']//8
        stride = self['rs2']//eew

        if 'start' in self:
            start = self['start']
        else:
            start = 0

        if 'mask' in self:
            mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
        else :
            mask = np.ones(self['vl'], dtype=np.uint8)
        
        if 'origin' in self:
            origin = self['origin']
        else:
            origin = np.zeros(vl, dtype=self['rs1'].dtype)
        
        tmp = np.zeros(stride*vl+1, dtype=self['rs1'].dtype)
        for i in range(vl):
            tmp[i*stride] = rs1[i]
        for i in range(start, vl):
            if mask[i] != 0:
                origin[i] = tmp[i*stride]

        return origin
