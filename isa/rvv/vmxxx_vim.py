from isa.inst import *
import numpy as np

class Vmadc_vim(Inst):
    name = 'vmadc.vim'
    # vmadc.vim vd, vs2, imm, v0  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit    = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        mask   = np.unpackbits(self['mask'],bitorder='little')
        vstart = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            carry = self['vs2'][ii].astype(object) + self['imm'].astype(object)  + mask[ii].astype(object) 
            bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0    
        result = np.packbits(bit, bitorder='little')   
        return result 
        