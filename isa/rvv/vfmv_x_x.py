from isa.inst import *
import numpy as np

class Vfmv_v_f(Inst):
    name = 'vfmv.v.f'

    def golden(self):

        vd = self['orig'].copy()

        for no in range(0, self['orig'].size):
            vd[no] = self['rs1'].astype(vd.dtype)[0]

        return vd

class Vfmv_s_f(Inst):
    name = 'vfmv.s.f'

    def golden(self):

        vd = self['orig'].copy()

        vd[0] = self['rs1'].astype(vd.dtype)[0]

        return vd

class Vfmv_f_s(Inst):
    name = 'vfmv.f.s'

    def golden(self):

        return self['orig'].astype(np.float32)[0]        
