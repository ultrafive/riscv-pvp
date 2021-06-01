from isa.inst import *
import numpy as np
import math

class Vlsegxex_v(Inst):
    name = 'vlsegxex.v'

    def golden(self):
        nf = self['nfields']
        vlen = self['vlen']
        assert int(self['rs1'].size / nf) == vlen
        return self.masked(self['rs1'].reshape((vlen, nf)).T).reshape((vlen * nf))
