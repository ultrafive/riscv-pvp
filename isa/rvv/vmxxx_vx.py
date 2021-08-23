from isa.inst import *
import numpy as np

class Vmseq_vx(Inst):
    name = 'vmseq.vx'
    # vmseq.vx vd, vs2, rs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if 'flag' in self:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                bit[ii] = 1 if self['vs2'][ii] == self['rs1'] else 0
        result = np.packbits(bit, bitorder='little')
        return result  


class Vmsne_vx(Inst):
    name = 'vmsne.vx'
    # vmsne.vx vd, vs2, rs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if 'flag' in self:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                bit[ii] = 1 if self['vs2'][ii] != self['rs1'] else 0
        result = np.packbits(bit, bitorder='little')
        return result 


class Vmslt_vx(Inst):
    name = 'vmslt.vx'
    # vmslt.vx vd, vs2, rs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if 'flag' in self:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                bit[ii] = 1 if self['vs2'][ii] < self['rs1'] else 0
        result = np.packbits(bit, bitorder='little')
        return result    

class Vmsltu_vx(Vmslt_vx):
    name = 'vmsltu.vx'


class Vmsle_vx(Inst):
    name = 'vmsle.vx'
    # vmsle.vx vd, vs2, rs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if 'flag' in self:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                bit[ii] = 1 if self['vs2'][ii] <= self['rs1'] else 0
        result = np.packbits(bit, bitorder='little')
        return result 
 
class Vmsleu_vx(Vmsle_vx):
    name = 'vmsleu.vx'


class Vmsgt_vx(Inst):
    name = 'vmsgt.vx'
    # vmsgt.vx vd, vs2, rs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if 'flag' in self:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                bit[ii] = 1 if self['vs2'][ii] > self['rs1'] else 0
        result = np.packbits(bit, bitorder='little')
        return result 

class Vmsgtu_vx(Vmsgt_vx):
    name = 'vmsgtu.vx'


class Vmadc_vx(Inst):
    name = 'vmadc.vx'
    # vmsbc.vx vd, vs2, rs1  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if 'flag' in self:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            carry = self['vs2'][ii].astype(object) + self['rs1'] 
            bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0 
        result = np.packbits(bit, bitorder='little')
        return result 


class Vmsbc_vx(Inst):
    name = 'vmsbc.vx'
    # vmsbc.vx vd, vs2, rs1  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if 'flag' in self:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            carry = self['vs2'][ii].astype(object) - self['rs1'] 
            bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0 
        result = np.packbits(bit, bitorder='little')
        return result 

