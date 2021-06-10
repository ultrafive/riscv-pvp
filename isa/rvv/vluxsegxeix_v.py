from isa.inst import *
import numpy as np
import math
class Vluxsegxeix_v(Inst):
    name = 'vluxsegxeix.v'

    def golden(self):
        nf = self['nfields']
        vlen = self['vlen']
        idx = (self['idx'] / self['rs1'].itemsize).astype(np.int)

        vlmax = int(self['lmul'] * self['VLEN'] / (self['rs1'].itemsize * 8))

        vds = self.masked(np.take(self['rs1'], idx[None].T + np.arange(nf)).T)
        vds = np.pad(vds, [(0,0),(0, int(vlmax - vlen))])
        return vds.reshape((vlmax * nf))
