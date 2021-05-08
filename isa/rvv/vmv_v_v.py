from isa.inst import *
import numpy as np

class Vmv_v_v(Inst):
    name = 'vmv.v.v'

    def golden(self):
        return self['vs1']