from isa.inst import *
import numpy as np
import math

factor_lmul = { 1:1, 2:2, 4:4, 8:8, 'f2':0.5, 'f4':0.25, 'f8':0.125}

class Vsssegxex_v(Inst):
    name = 'vsssegxex.v'

    def golden(self):

        if 'isExcept' in self:
            if self['isExcept'] > 0:
                return np.zeros(1024*8//(self['vs3'].itemsize*8), dtype=self['vs3'].dtype)
        nf = self['nf']
        vlen = self['vlen']
        emul = self['eew'] /self['sew']*factor_lmul[self['lmul']]
        emul = 1 if emul < 1 else int(emul)
        vlmax = int(emul * self['VLEN'] // (self['vs3'].itemsize*8))
        eew = self['eew']//8
        stride = self['rs2']//eew

        vs3 = self['vs3'][0: vlmax*nf].reshape(nf, vlmax)[:, 0:vlen]

        if 'start' in self:
            start = self['start']
        else:
            start = 0
        
        if 'origin' in self:
            origin = self['origin']
        else:
            origin = np.zeros(self['VLEN']*8//(self['vs3'].itemsize*8), dtype=self['vs3'].dtype)
        
        if 'mask' in self:
            mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vlen']]
        else :
            mask = np.ones(self['vlen'], dtype=np.uint8)

        if self['rs2'] >= eew*nf:
            for i in range(nf):
                origin[start*nf+i: vlen*nf+i: nf] = self.masked(vs3[i], origin[i: vlen*nf+i: nf])[start: vlen]
        else:
            tmp = self['origin'] if 'origin' in self else np.zeros(self['VLEN']*8//(self['vs3'].itemsize*8), dtype=self['vs3'].dtype)
            for i in range(start, vlen):
                if mask[i] != 0:
                    tmp[i*stride: i*stride+nf] = vs3[:,i]
            for i in range(vlen):
                    origin[i*nf: i*nf+nf] = tmp[i*stride: i*stride+nf]

        return origin