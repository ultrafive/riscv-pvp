from ...isa.inst import *
import numpy as np

class Vssra_vv(Inst):
    name = 'vssra.vv'
    # vssra.vv vd, vs2, vs1, vm  
    # vd[i] = roundoff_unsigned(vs2[i], vs1[i])
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
  
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['vs1'][ii] % self['sew']
                result[ii] = self.rounding_xrm( self['vs2'][ii], vxrm, shift )               
        return result 

class Vssrl_vv(Inst):
    name = 'vssrl.vv'
    # vssrl.vv vd, vs2, vs1, vm  
    # vd[i] = roundoff_signed(vs2[i], vs1[i])
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
  
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['vs1'][ii] % self['sew']
                result[ii] = self.rounding_xrm( self['vs2'][ii], vxrm, shift )               
        return result 


class Vssra_vx(Inst):
    name = 'vssra.vx'
    # vssra.vx vd, vs2, rs1, vm 
    # vd[i] = roundoff_signed(vs2[i], x[rs1])  
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
  
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['rs1'] % self['sew']   
                result[ii] = self.rounding_xrm( self['vs2'][ii], vxrm, shift )               
        return result 

class Vssrl_vx(Inst):
    name = 'vssrl.vx'
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
  
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['rs1'] % self['sew']   
                result[ii] = self.rounding_xrm( self['vs2'][ii], vxrm, shift )               
        return result   


class Vssra_vi(Inst):
    name = 'vssra.vi'
    # vssra.vi vd, vs2, uimm, vm  
    # vd[i] = roundoff_signed(vs2[i], uimm) 
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
  
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['uimm'] % self['sew']   #np.fmod(self['rs1'], self['sew']) # %
                result[ii] = self.rounding_xrm( self['vs2'][ii], vxrm, shift )               
        return result 

class Vssrl_vi(Inst):
    name = 'vssrl.vi'
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 
  
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                shift = self['uimm'] % self['sew']  
                result[ii] = self.rounding_xrm( self['vs2'][ii], vxrm, shift )               
        return result 

