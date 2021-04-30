from isa.inst import *
import numpy as np

class Vfmv_v_f(Inst):
    name = 'vfmv.v.f'

    def golden(self):

        vd = self['orig'].copy()

        for no in range(0, self['orig'].size):
            vd[no] = self['rs1'].astype(vd.dtype)[0]

        return vd