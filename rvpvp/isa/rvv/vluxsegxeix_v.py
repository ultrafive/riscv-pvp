from ...isa.inst import *
import numpy as np
import math

factor_lmul = { 1:1, 2:2, 4:4, 8:8, 'f2':0.5, 'f4':0.25, 'f8':0.125}

class Vluxsegxeix_v(Inst):
    name = 'vluxsegxeix.v'

    def golden(self):
        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(1024*8//(self['rs1'].itemsize*8), dtype=self['rs1'].dtype)
        nf = self['nf']
        vl = self['vl']
        lmul = 1 if factor_lmul[self['lmul']] < 1 else factor_lmul[self['lmul']]
        vlmax = int(self['VLEN']*lmul//self['sew'])

        rs1 = self['rs1'].reshape(vl, nf)
        index = self['vs2']

        if 'start' in self:
            start = self['start']
        else:
            start = 0

        if 'mask' in self:
            mask_src = self['mask']
            mask_src.dtype = np.uint8
            mask = np.unpackbits(mask_src, bitorder='little')[0: self['vl']]
        else :
            mask = np.ones(self['vl'], dtype=np.uint8)
        
        if 'origin' in self:
            origin = self['origin']
        else:
            origin = np.zeros(self['VLEN']*8//(self['rs1'].itemsize*8), dtype=self['rs1'].dtype)
        
        tmp = np.zeros(int(np.max(self['vs2'])//self['rs1'].itemsize+nf), dtype=self['rs1'].dtype)
        for i in range(vl):
            curIdx = int(index[i] // self['rs1'].itemsize)
            tmp[curIdx: curIdx+nf] = rs1[i]
                
        for i in range(start, vl):
            curIdx = int(index[i] // self['rs1'].itemsize)
            if mask[i] != 0:
                try:
                    origin[i: i+nf*vlmax: vlmax] = tmp[curIdx: curIdx+nf]
                except ValueError:
                    print(origin.shape, i, nf, lmul, vlmax)

        return origin