from isa.inst import *
import numpy as np
import math

factor_lmul = { 1:1, 2:2, 4:4, 8:8, 'f2':0.5, 'f4':0.25, 'f8':0.125}

class Vlssegxex_v(Inst):
    name = 'vlssegxex.v'

    def golden(self):
        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(1024*8//(self['rs1'].itemsize*8), dtype=self['rs1'].dtype)
        nf = self['nf']
        vlen = self['vlen']
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
            mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vlen']]
        else :
            mask = np.ones(self['vlen'], dtype=np.uint8)
        
        if 'origin' in self:
            origin = self['origin']
        else:
            origin = np.zeros(self['VLEN']*8//(self['rs1'].itemsize*8), dtype=self['rs1'].dtype)
        
        tmp = np.zeros(vlen*stride+nf, dtype=self['rs1'].dtype)

        for i in range(vlen):
            tmp[i*stride: i*stride+nf] = rs1[i*nf: i*nf+nf]

        for i in range(start, vlen):
            if mask[i] != 0:
                origin[i: (nf-1)*vlmax+i+1: vlmax] = tmp[i*stride: i*stride+nf]

        return origin
