from isa.inst import *
import numpy as np

class Vmadc_vvm(Inst):
    name = 'vmadc.vvm'
    # vmadc.vvm vd, vs2, vs1, v0  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if 'flag' in self:
            print("ori = "+str(self['ori']))
            self['ori'].dtype = np.uint8
        bit    = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        print("bit = "+str(bit))
        mask   = np.unpackbits(self['mask'],bitorder='little')
        vstart = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            carry = self['vs2'][ii].astype(object) + self['vs1'][ii].astype(object) + mask[ii].astype(object) 
            bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0  
        result = np.packbits(bit, bitorder='little')
        return result 


class Vmsbc_vvm(Inst):
    name = 'vmsbc.vvm'
    # vmsbc.vvm vd, vs2, vs1, v0  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if 'flag' in self:
            self['ori'].dtype = np.uint8
        bit    = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']] 
        mask   = np.unpackbits(self['mask'],bitorder='little')
        vstart = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            carry = self['vs2'][ii].astype(object) - self['vs1'][ii].astype(object) - mask[ii].astype(object) 
            bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0  
        result = np.packbits(bit, bitorder='little')   
        return result 
