from ...isa.inst import *
import numpy as np
import math

class Vadd_vv(Inst):
    name = 'vadd.vv'
    # vadd.vv vd, vs2, vs1, vm
    def golden(self):
        result = self['ori'].copy()
        if self['vl']==0:
            return self['ori']
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]+self['vs1'][ii]
        return result


class Vsub_vv(Inst):
    name = 'vsub.vv'
    # vsub.vv vd, vs2, vs1, vm
    def golden(self):
        result = self['ori'].copy()
        if self['vl']==0:
            return self['ori']
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]-self['vs1'][ii]
        return result


class Vand_vv(Inst):
    name = 'vand.vv'
    # vand.vv vd, vs2, vs1, vm 
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] & self['vs1'][ii]
        return result


class Vor_vv(Inst):
    name = 'vor.vv'
    # vor.vv vd, vs2, vs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] | self['vs1'][ii]
        return result


class Vxor_vv(Inst):
    name = 'vxor.vv'
    # vxor.vv vd, vs2, vs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] ^ self['vs1'][ii]
        return result


class Vmin_vv(Inst):
    name = 'vmin.vv'
    # vmin.vv vd, vs2, vs1, vm  
    def golden(self):
        result = self['ori'].copy()
        if self['vl']==0:
            return self['ori']
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = min(self['vs2'][ii],self['vs1'][ii])   # np.minimum
        return result

class Vminu_vv(Vmin_vv):
    name = 'vminu.vv'


class Vmax_vv(Inst):
    name = 'vmax.vv'
    # vmax.vv vd, vs2, vs1, vm  
    def golden(self):
        result = self['ori'].copy()
        if self['vl']==0:
            return self['ori']
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = max(self['vs2'][ii],self['vs1'][ii])
        return result

class Vmaxu_vv(Vmax_vv):
    name = 'vmaxu.vv'


class Vmul_vv(Inst):
    name = 'vmul.vv'
    # vmul.vv vd, vs2, vs1, vm  
    def golden(self):
        result = self['ori'].copy()
        if self['vl']==0:
            return self['ori']
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]*self['vs1'][ii]
        return result


class Vmulh_vv(Inst):
    name = 'vmulh.vv'
    # vmulh.vv vd, vs2, vs1, vm 
    def golden(self):      
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):                
                result_tmp = self['vs2'][ii].astype(object)* self['vs1'][ii].astype(object)
                result[ii] = result_tmp >> self['sew']
        return result

class Vmulhu_vv(Vmulh_vv):
    name = 'vmulhu.vv'

class Vmulhsu_vv(Vmulh_vv):
    name = 'vmulhsu.vv'


class Vdiv_vv(Inst):
    name = 'vdiv.vv'
    #  vdiv.vv vd, vs2, vs1, vm  
    def golden(self):
        INT64_MIN = (-(9223372036854775807)-1)
        result = self['ori'].copy()
        if self['vl']==0:
            return self['ori']
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['vs1'][ii] == 0:
                    result[ii] = -1
                elif (self['vs2'][ii] == (INT64_MIN>>(64-self['sew']))) and (self['vs1'][ii] == -1):
                    result[ii] = self['vs2'][ii] 
                else:
                    result[ii] = self['vs2'][ii] / self['vs1'][ii]
        return result


class Vdivu_vv(Inst):
    name = 'vdivu.vv'
    #  vdivu.vv vd, vs2, vs1, vm  
    def golden(self):
        result = self['ori'].copy()
        if self['vl']==0:
            return self['ori']
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['vs1'][ii] == 0:
                    result[ii] = -1
                else:
                    result[ii] = self['vs2'][ii] / self['vs1'][ii]
        return result


class Vrem_vv(Inst):
    name = 'vrem.vv'
    # vrem.vv vd, vs2, vs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        INT64_MIN = (-(9223372036854775807)-1)
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['vs1'][ii] == 0:
                    result[ii] = self['vs2'][ii]
                elif (self['vs2'][ii] == (INT64_MIN>>(64-self['sew']))) and (self['vs1'][ii] == -1):
                    result[ii] = 0 
                else:
                    result[ii] = np.fmod(self['vs2'][ii] , self['vs1'][ii]) #note %
        return result


class Vremu_vv(Inst):
    name = 'vremu.vv'
    # vremu.vv vd, vs2, vs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['vs1'][ii] == 0:
                    result[ii] = self['vs2'][ii]
                else:
                    result[ii] = np.fmod(self['vs2'][ii] , self['vs1'][ii]) 
        return result


class Vsll_vv(Inst):
    name = 'vsll.vv'
    # vsll.vv vd, vs2, vs1, vm  ## left logic  >>
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = np.left_shift(self['vs2'][ii].astype(object) , (self['vs1'][ii]%self['sew']))
        return result


class Vsrl_vv(Inst):
    name = 'vsrl.vv'
    # vsrl.vv vd, vs2, vs1, vm 
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) >> (self['vs1'][ii]%self['sew']) 
        return result

class Vsra_vv(Vsrl_vv):
    name = 'vsra.vv'
    # vsra.vv vd, vs2, vs1, vm


