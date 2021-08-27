from isa.inst import *
import numpy as np

class Vaadd_vv(Inst):
    name = 'vaadd.vv'
    # vaadd.vv vd, vs2, vs1, vm 
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
            
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                tmp = np.add(self['vs2'][ii],self['vs1'][ii],dtype='object')
                result[ii] = self.rounding_xrm( tmp, vxrm, 1 )
        return result 

class Vaaddu_vv(Vaadd_vv):
    name = 'vaaddu.vv'


class Vasub_vv(Inst):
    name = 'vasub.vv'
    # vasub.vv vd, vs2, vs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
            
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                tmp = np.subtract(self['vs2'][ii],self['vs1'][ii],dtype='object')
                result[ii] = self.rounding_xrm( tmp, vxrm, 1 )
        return result       

class Vasubu_vv(Vasub_vv):
    name = 'vasubu.vv'


class Vaadd_vx(Inst):
    name = 'vaadd.vx'
    # vaadd.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
            
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                tmp = np.add(self['vs2'][ii],self['rs1'],dtype='object')
                result[ii] = self.rounding_xrm( tmp, vxrm, 1 )
        return result 

class Vaaddu_vx(Vaadd_vx):
    name = 'vaaddu.vx'


class Vasub_vx(Inst):
    name = 'vasub.vx'
    # vasub.vx vd, vs2, rs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
            
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                tmp = np.subtract(self['vs2'][ii],self['rs1'],dtype='object')
                result[ii] = self.rounding_xrm( tmp, vxrm, 1 )
        return result     


class Vasubu_vx(Vasub_vx):
    name = 'vasubu.vx'
