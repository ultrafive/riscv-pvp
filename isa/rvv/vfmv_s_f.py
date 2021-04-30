from isa.inst import *
import numpy as np

class Vfmv_s_f(Inst):
    name = 'vfmv.s.f'

    def golden(self):

        vd = self['orig'].copy()

        vd[0] = self['rs1'].astype(vd.dtype)[0]

        return vd