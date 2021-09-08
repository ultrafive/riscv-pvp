from ...isa.inst import *
import numpy as np

class Vmseq_vi(Inst):
    name = 'vmseq.vi'
    # vmseq.vi vd, vs2, imm, vm 
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
                bit[ii] = 1 if self['vs2'][ii] == self['imm'] else 0
        result = np.packbits(bit, bitorder='little')
        return result      


class Vmsne_vi(Inst):
    name = 'vmsne.vi'
    # vmsne.vi vd, vs2, imm, vm  
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
                bit[ii] = 1 if self['vs2'][ii] != self['imm'] else 0
        result = np.packbits(bit, bitorder='little')
        return result 


class Vmsle_vi(Inst):
    name = 'vmsle.vi'
    # vmsle.vi vd, vs2, imm, vm  
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
                bit[ii] = 1 if self['vs2'][ii] <= self['imm'] else 0
        result = np.packbits(bit, bitorder='little')
        return result 

class Vmsleu_vi(Vmsle_vi):  #res = vs2 <= (insn.v_simm5() & (UINT64_MAX >> (64 - P.VU.vsew)));
    name = 'vmsleu.vi'


class Vmsgt_vi(Inst):
    name = 'vmsgt.vi'
    # vmsgt.vi vd, vs2, imm, vm  
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
                bit[ii] = 1 if self['vs2'][ii] > self['imm'] else 0
        result = np.packbits(bit, bitorder='little')
        return result 

class Vmsgtu_vi(Vmsgt_vi):
    name = 'vmsgtu.vi'


class Vmadc_vi(Inst):
    name = 'vmadc.vi'

    def golden(self):     
        if self['vl']==0:
            return self['ori']
        if self['ori'].dtype != np.uint8:
            self['ori'].dtype = np.uint8
        bit  = np.unpackbits(self['ori'], bitorder='little')[0:8*self['bvl']]  
        vstart = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            carry = self['vs2'][ii].astype(object) + self['imm'] 
            bit[ii] = 1 if ((carry>>self['sew']) & 1) else 0 
        result = np.packbits(bit, bitorder='little')
        return result 

