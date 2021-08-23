from isa.inst import *
import numpy as np

class Vmv_v_x(Inst):
    name = 'vmv.v.x'
    # vmv.v.x vd, rs1  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            result[ii] = self['rs1']
        return result 
