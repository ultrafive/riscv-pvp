from isa.inst import *
import numpy as np
import math

class Vlsegxex_v(Inst):
    name = 'vlsegxex.v'

    def golden(self):
        nf = self['nfields']
        vl = self['vl']
        assert int(self['rs1'].size / nf) == vl

        vlmax = int(self['lmul'] * self['VLEN'] / (self['rs1'].itemsize * 8))

        vds = self.masked(self['rs1'].reshape((vl, nf)).T)
        vds = np.pad(vds, [(0,0),(0, int(vlmax - vl))])
        return vds.reshape((vlmax * nf))
