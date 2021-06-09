from isa.inst import *
import numpy as np
import math
class Vlssegxex_v(Inst):
    name = 'vlssegxex.v'

    def golden(self):
        nf = self['nfields']
        vlen = self['vlen']
        stride = int(self['stride']/self['rs1'].itemsize)
        assert int(self['rs1'].size / stride) == vlen
        assert stride >= nf

        vlmax = int(self['lmul'] * self['VLEN'] / (self['rs1'].itemsize * 8))

        vds = self.masked(self['rs1'].reshape((vlen, stride))[:,:nf].T)
        vds = np.pad(vds, [(0,0),(0, int(vlmax - vlen))])
        return vds.reshape((vlmax * nf))
