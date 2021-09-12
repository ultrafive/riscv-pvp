from ...isa.inst import *
import numpy as np
import math

##               uint8  -->  bit  -->  uint8 --> (u)intSEW
##  (vector_mask_array_random)   (unpackbits)(packbits)   (dtype)
class Vmseq_vv(Inst):
    name = 'vmseq.vv'
    # vmseq.vv vd, vs2, vs1, vm 
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                bit[ii] = 1 if self['vs2'][ii] == self['vs1'][ii] else 0
        result = np.packbits(bit, bitorder='little')
        return result 


class Vmsne_vv(Inst):
    name = 'vmsne.vv'
    # vmsne.vv vd, vs2, vs1, vm 
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                bit[ii] = 1 if self['vs2'][ii] != self['vs1'][ii] else 0
        result = np.packbits(bit, bitorder='little')
        return result 


class Vmslt_vv(Inst):
    name = 'vmslt.vv'
    # vmslt.vv vd, vs2, vs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                bit[ii] = 1 if self['vs2'][ii] < self['vs1'][ii] else 0
        result = np.packbits(bit, bitorder='little')
        return result 

class Vmsltu_vv(Vmslt_vv):
    name = 'vmsltu.vv'


class Vmsle_vv(Inst):
    name = 'vmsle.vv'
    # vmsle.vv vd, vs2, vs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                bit[ii] = 1 if self['vs2'][ii] <= self['vs1'][ii] else 0
        result = np.packbits(bit, bitorder='little')
        return result 

class Vmsleu_vv(Vmsle_vv):
    name = 'vmsleu.vv'


class Vmadc_vv(Inst):
    name = 'vmadc.vv'
    # vmadc.vv vd, vs2, vs1 
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                carry = self['vs2'][ii].astype(object) + self['vs1'][ii].astype(object) 
                bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0 
        result = np.packbits(bit, bitorder='little')
        return result     


class Vmsbc_vv(Inst):
    name = 'vmsbc.vv'
    # vmsbc.vv vd, vs2, vs1 
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                carry = self['vs2'][ii].astype(object) - self['vs1'][ii].astype(object) 
                bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0 
        result = np.packbits(bit, bitorder='little')
        return result 

