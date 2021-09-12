from ...isa.inst import *
import numpy as np
import math

class Vssex_v(Inst):
    name = 'vssex.v'

    def golden(self):

        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(self['vl'], dtype=self['vs3'].dtype)
        vl = self['vl']
        emul = self['eew'] /self['sew']*factor_lmul[self['lmul']]
        emul = 1 if emul < 1 else int(emul)
        vlmax = int(emul * self['VLEN'] // (self['vs3'].itemsize*8))
        eew = self['eew']//8
        stride = self['rs2']//eew

        vs3 = self['vs3']

        if 'start' in self:
            start = self['start']
        else:
            start = 0
        
        if 'origin' in self:
            origin = self['origin']
        else:
            origin = np.zeros(vl, dtype=self['vs3'].dtype)
        
        if 'mask' in self:
            mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
        else :
            mask = np.ones(self['vl'], dtype=np.uint8)

        if stride == 0:
            tmp = 0
            for i in range(start, vl):
                if mask[i] != 0:
                    tmp = vs3[i]
            origin[0: vl] = tmp        
        else:
            origin[start: vl] = self.masked(vs3[0:vl], origin[0: vl])[start: vl]

        return origin
