from ...isa.inst import *
import numpy as np
import math

class Vsssegxex_v(Inst):
    name = 'vsssegxex.v'

    def golden(self):

        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(1024*8//(self['vs3'].itemsize*8), dtype=self['vs3'].dtype)
        nf = self['nf']
        vl = self['vl']
        emul = self['eew'] /self['sew']*factor_lmul[self['lmul']]
        emul = 1 if emul < 1 else int(emul)
        vlmax = int(emul * self['VLEN'] // (self['vs3'].itemsize*8))
        eew = self['eew']//8
        stride = self['rs2']//eew

        vs3 = self['vs3'][0: vlmax*nf].reshape(nf, vlmax)[:, 0:vl]

        if 'start' in self:
            start = self['start']
        else:
            start = 0
        
        if 'origin' in self:
            origin = self['origin']
        else:
            origin = np.zeros(self['VLEN']*8//(self['vs3'].itemsize*8), dtype=self['vs3'].dtype)
        
        if 'mask' in self:
            mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
        else :
            mask = np.ones(self['vl'], dtype=np.uint8)

        if self['rs2'] >= eew*nf:
            for i in range(nf):
                origin[start*nf+i: vl*nf+i: nf] = self.masked(vs3[i], origin[i: vl*nf+i: nf])[start: vl]
        else:
            tmp = self['origin'] if 'origin' in self else np.zeros(self['VLEN']*8//(self['vs3'].itemsize*8), dtype=self['vs3'].dtype)
            for i in range(start, vl):
                if mask[i] != 0:
                    tmp[i*stride: i*stride+nf] = vs3[:,i]
            for i in range(vl):
                    origin[i*nf: i*nf+nf] = tmp[i*stride: i*stride+nf]

        return origin