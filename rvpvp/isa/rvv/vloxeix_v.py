from ...isa.inst import *
import numpy as np
import math

class Vloxeix_v(Inst):
    name = 'vloxeix.v'

    def golden(self):
        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(self['vl'], dtype=self['rs1'].dtype)
        vl = self['vl']
        lmul = 1 if factor_lmul[self['lmul']] < 1 else factor_lmul[self['lmul']]
        vlmax = int(self['VLEN']*lmul//self['sew'])

        rs1 = self['rs1']
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
            mask = np.ones(vl, dtype=np.uint8)
        
        if 'origin' in self:
            origin = self['origin']
        else:
            origin = np.zeros(vl, dtype=self['rs1'].dtype)
        
        tmp = np.zeros(int(np.max(self['vs2'])//self['rs1'].itemsize+1), dtype=self['rs1'].dtype)
        for i in range(vl):
            curIdx = int(index[i] // self['rs1'].itemsize)
            tmp[curIdx] = rs1[i]
                
        for i in range(start, vl):
            curIdx = int(index[i] // self['rs1'].itemsize)
            if mask[i] != 0:
                origin[i] = tmp[curIdx]

        return origin
