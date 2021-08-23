from isa.inst import *
import numpy as np

class Vadc_vvm(Inst):
    name = 'vadc.vvm'
    # vadc.vvm vd, vs2, vs1, v0  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart = self['vstart'] if 'vstart' in self else 0 
        mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
        for ii in range(vstart, self['vl']): 
            result[ii] = self['vs2'][ii].astype(object) + self['vs1'][ii] + mask[ii]
        return result 


class Vsbc_vvm(Inst):
    name = 'vsbc.vvm'
    # vsbc.vvm vd, vs2, vs1, v0  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart = self['vstart'] if 'vstart' in self else 0 
        mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
        for ii in range(vstart, self['vl']): 
            result[ii] = self['vs2'][ii].astype(object) - self['vs1'][ii] - mask[ii]
        return result 


class Vmerge_vvm(Inst):
    name = 'vmerge.vvm'
    # vmerge.vvm vd, vs2, vs1, v0  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart = self['vstart'] if 'vstart' in self else 0 
        mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
        for ii in range(vstart, self['vl']): 
            result[ii] = self['vs1'][ii] if mask[ii] else self['vs2'][ii]
        return result 
