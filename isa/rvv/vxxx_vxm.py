from isa.inst import *
import numpy as np

class Vadc_vxm(Inst):
    name = 'vadc.vxm'
    # vadc.vxm vd, vs2, rs1, v0   
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart = self['vstart'] if 'vstart' in self else 0 
        mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']] 
        for ii in range(vstart, self['vl']): 
            result[ii] = self['vs2'][ii].astype(object) + self['rs1'] + mask[ii]
        return result 


class Vsbc_vxm(Inst):
    name = 'vsbc.vxm'
    # vsbc.vxm vd, vs2, rs1, v0 
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart = self['vstart'] if 'vstart' in self else 0 
        mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
        for ii in range(vstart, self['vl']): 
            result[ii] = self['vs2'][ii].astype(object) - self['rs1'] - mask[ii]
        return result 


class Vmerge_vxm(Inst):
    name = 'vmerge.vxm'
    # vmerge.vxm vd, vs2, rs1, v0   
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart = self['vstart'] if 'vstart' in self else 0 
        mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
        for ii in range(vstart, self['vl']): 
            result[ii] = self['rs1'] if mask[ii] else self['vs2'][ii]
        return result 

