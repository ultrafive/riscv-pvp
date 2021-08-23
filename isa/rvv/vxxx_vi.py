from isa.inst import *
import numpy as np

class Vadd_vi(Inst):
    name = 'vadd.vi'
    # vadd.vi vd, vs2, imm, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]+self['imm']
        return result


class Vrsub_vi(Inst):
    name = 'vrsub.vi'
    # vrsub.vi vd, vs2, imm, vm   
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['imm'] - self['vs2'][ii]
        return result


class Vand_vi(Inst):
    name = 'vand.vi'
    # vand.vi vd, vs2, imm, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] & self['imm']
        return result


class Vor_vi(Inst):
    name = 'vor.vi'
    # vor.vi vd, vs2, imm, vm   
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] | self['imm']
        return result


class Vxor_vi(Inst):
    name = 'vxor.vi'
    # vxor.vi vd, vs2, imm, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] ^ self['imm']
        return result


class Vsll_vi(Inst):
    name = 'vsll.vi'
    # vsll.vi vd, vs2, uimm, vm      ## left logic  >>
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = np.left_shift(self['vs2'][ii], (self['imm']%self['sew']))
        return result


class Vsrl_vi(Inst):
    name = 'vsrl.vi'
    # vsrl.vi vd, vs2, uimm, vm    
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] >> (self['imm']%self['sew']) 
        return result

class Vsra_vi(Vsrl_vi):
    name = 'vsra.vi'
    # vsra.vi vd, vs2, uimm, vm  
