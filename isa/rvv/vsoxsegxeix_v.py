from isa.inst import *
import numpy as np
import math

factor_lmul = { 1:1, 2:2, 4:4, 8:8, 'f2':0.5, 'f4':0.25, 'f8':0.125}

class Vsoxsegxeix_v(Inst):
    name = 'vsoxsegxeix.v'

    def golden(self):
        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(1024*8//(self['vs3'].itemsize*8), dtype=self['vs3'].dtype)
        nf = self['nf']
        vl = self['vl']
        lmul = 1 if factor_lmul[self['lmul']] < 1 else factor_lmul[self['lmul']]
        vlmax = int(self['VLEN']*lmul//self['sew'])

        vs3 = self['vs3'][0:vlmax*nf].reshape(nf, vlmax).T
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
            origin = np.zeros(self['VLEN']*8//(self['vs3'].itemsize*8), dtype=self['vs3'].dtype)
        
        tmp = np.zeros(int(np.max(self['vs2'])//self['vs3'].itemsize+nf), dtype=self['vs3'].dtype)
        for i in range(start, vl):
            if mask[i] != 0:
                curIdx = int(index[i] // self['vs3'].itemsize)
                tmp[curIdx: curIdx+nf] = vs3[i]
                
        for i in range(start, vl):
            curIdx = int(index[i] // self['vs3'].itemsize)
            origin[i*nf: i*nf+nf] = tmp[curIdx: curIdx+nf]


        return origin