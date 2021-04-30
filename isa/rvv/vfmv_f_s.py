from isa.inst import *
import numpy as np

class Vfmv_f_s(Inst):
    name = 'vfmv.f.s'

    def golden(self):

        return self['orig'].astype(np.float32)[0]