from ...isa.inst import *
import numpy as np

class Vmv_v_i(Inst):
    name = 'vmv.v.i'
    # vmv.v.i vd, imm   
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            result[ii] = self['imm']
        return result 
