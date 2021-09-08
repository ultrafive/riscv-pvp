from ...isa.inst import *
import numpy as np

class Vmv_v_v(Inst):
    name = 'vmv.v.v'
    # vmv.v.v vd, vs1     
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            result[ii] = self['vs1'][ii]
        return result 
