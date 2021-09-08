from ...isa.inst import *
import numpy as np

class Vmv_s_x(Inst):
    name = 'vmv.s.x'
    # vmv.s.x vd, rs1 # vd[0] = x[rs1] (vs2=0)
    def golden(self):
        vstart = self['vstart'] if 'vstart' in self else 0
        if vstart >=  self['vl']:
            return self['vd'][0]
        return self['rs1']
