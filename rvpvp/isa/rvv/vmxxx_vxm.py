from ...isa.inst import *
import numpy as np

class Vmadc_vxm(Inst):
    name = 'vmadc.vxm'
    # vmadc.vxm vd, vs2, rs1, v0  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit    = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        mask   = np.unpackbits(self['mask'],bitorder='little')
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            carry = self['vs2'][ii].astype(object) + self['rs1'].astype(object)  + mask[ii].astype(object) 
            bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0    
        result = np.packbits(bit, bitorder='little')   
        return result 


class Vmsbc_vxm(Inst):
    name = 'vmsbc.vxm'
    # vmsbc.vxm vd, vs2, rs1, v0  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit    = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        mask   = np.unpackbits(self['mask'],bitorder='little')
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            carry = self['vs2'][ii].astype(object) - self['rs1'].astype(object)  - mask[ii].astype(object) 
            bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0    
        result = np.packbits(bit, bitorder='little')    
        return result 
        