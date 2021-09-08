from ...isa.inst import *
import numpy as np

class Vadd_vx(Inst):
    name = 'vadd.vx'
    # vadd.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]+self['rs1']
        return result


class Vsub_vx(Inst):
    name = 'vsub.vx'
    #  vsub.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]-self['rs1']
        return result


class Vrsub_vx(Inst):
    name = 'vrsub.vx'
    # vrsub.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['rs1'] - self['vs2'][ii]  #note 0-intmin
        return result


class Vmin_vx(Inst):
    name = 'vmin.vx'
    # vmin.vx vd, vs2, rs1, vm   
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = min(self['rs1'], self['vs2'][ii])  
        return result

class Vminu_vx(Vmin_vx):
    name = 'vminu.vx'


class Vmax_vx(Inst):
    name = 'vmax.vx'
    # vmax.vx vd, vs2, rs1, vm   
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = np.maximum(self['rs1'], self['vs2'][ii])  
        return result

class Vmaxu_vx(Vmax_vx):
    name = 'vmaxu.vx'


class Vand_vx(Inst):
    name = 'vand.vx'
    # vand.vx vd, vs2, rs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] & self['rs1']
        return result


class Vor_vx(Inst):
    name = 'vor.vx'
    # vor.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] | self['rs1']
        return result


class Vxor_vx(Inst):
    name = 'vxor.vx'
    # vxor.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] ^ self['rs1']
        return result


class Vsll_vx(Inst):
    name = 'vsll.vx'
    # vsll.vx vd, vs2, rs1, vm    ## left logic  >>
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = np.left_shift(self['vs2'][ii], (self['rs1']%self['sew']))
        return result


class Vsrl_vx(Inst):
    name = 'vsrl.vx'
    # vsrl.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii] >> (self['rs1']%self['sew']) 
        return result

class Vsra_vx(Vsrl_vx):
    name = 'vsra.vx'
    # vsra.vx vd, vs2, rs1, vm  


class Vmul_vx(Inst):
    name = 'vmul.vx'
    # vmul.vx vd, vs2, rs1, vm   
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]*self['rs1']
        return result


class Vmulh_vx(Inst):
    name = 'vmulh.vx'
    # vmulh.vx vd, vs2, rs1, vm  
    def golden(self):      
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):                
                result[ii] = self['vs2'][ii].astype(object) * self['rs1'] // (2**self['sew']) # note: 'right_shift', rule 'safe'
        return result

class Vmulhu_vx(Vmulh_vx):
    name = 'vmulhu.vx'

class Vmulhsu_vx(Vmulh_vx):
    name = 'vmulhsu.vx'


class Vdiv_vx(Inst):
    name = 'vdiv.vx'
    # vdiv.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        INT64_MIN = (-(9223372036854775807)-1)
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['rs1'] == 0:
                    result[ii] = -1
                elif (self['vs2'][ii] == (INT64_MIN>>(64-self['sew']))) and (self['rs1'] == -1):
                    result[ii] = self['vs2'][ii] 
                else:
                    result[ii] = self['vs2'][ii] / self['rs1']
        return result


class Vdivu_vx(Inst):
    name = 'vdivu.vx'
    # vdivu.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['rs1'] == 0:
                    result[ii] = -1
                else:
                    result[ii] = self['vs2'][ii] // self['rs1'] #note "/"
        return result


class Vrem_vx(Inst):
    name = 'vrem.vx'
    # vrem.vx vd, vs2, rs1, vm   
    def golden(self):
        if self['vl']==0:
            return self['ori']
        INT64_MIN = (-(9223372036854775807)-1)
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['rs1'] == 0:
                    result[ii] = self['vs2'][ii]
                elif (self['vs2'][ii] == (INT64_MIN>>(64-self['sew']))) and (self['rs1'] == -1):
                    result[ii] = 0 
                else:
                    result[ii] = np.fmod(self['vs2'][ii] , self['rs1']) #note %
        return result
 

class Vremu_vx(Inst):
    name = 'vremu.vx'
    # vremu.vx vd, vs2, rs1, vm   
    def golden(self):        
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if self['rs1'] == 0:
                    result[ii] = self['vs2'][ii]
                else:
                    result[ii] = np.fmod(self['vs2'][ii] , self['rs1'])
        return result
