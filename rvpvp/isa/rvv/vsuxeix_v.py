from ...isa.inst import *
import numpy as np
import math

class Vsuxeix_v(Inst):
    name = 'vsuxeix.v'

    def golden(self):
        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(self['vl'], dtype=self['vs3'].dtype)
        
        vs3 = self['vs3'].copy()
        vs3.dtype = np.uint8
        sew = self['sew'] // 8

        index = self['vs2']

        if 'start' in self:
            start = self['start']
        else:
            start = 0
        
        if 'offset' in self:
            offset = self['offset']
        else :
            offset = 0

        if 'origin' in self:
            origin = self['origin']
        else:
            origin = np.zeros( self['vl'], dtype=self['vs3'].dtype )

        origin.dtype = np.uint8

        if 'mask' in self:
            mask = self['mask'].copy()
            mask.dtype = np.uint8
            mask_bits = np.unpackbits(mask, bitorder='little')[0: self['vl']]
        else:
            mask_bits = np.ones(self['vl'], dtype=np.uint8)

        tmp = np.zeros(int((np.max(self['vs2'])+sew)*sew), dtype=np.uint8)

        for no in range(start, self['vl']):
            curIdx = int(offset+index[no])
            if mask_bits[no] != 0:
                tmp[curIdx: curIdx+sew] = vs3[no*sew: no*sew+sew]

        for no in range(start, self['vl']):
            curIdx = int(offset+index[no])
            origin[no*sew: no*sew+sew] = tmp[curIdx: curIdx+sew]
        
        origin.dtype = self['vs3'].dtype

        return origin

class Vsuxei8_v(Vsuxeix_v):
    name = 'vsuxei8.v'

class Vsuxei16_v(Vsuxeix_v):
    name = 'vsuxei16.v'



class Vsuxei32_v(Vsuxeix_v):
    name = 'vsuxei32.v'



class Vsuxei64_v(Vsuxeix_v):
    name = 'vsuxei64.v'


