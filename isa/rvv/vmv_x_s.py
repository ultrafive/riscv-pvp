from isa.inst import *
import numpy as np

class Vmv_x_s(Inst):
    name = 'vmv.x.s'
    # vmv.x.s rd, vs2 
    # x[rd] = vs2[0] (vs1=0)
    def golden(self):
        return self['vs2'][0]
