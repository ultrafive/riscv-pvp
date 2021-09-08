from ...isa.inst import *
import numpy as np

class Vsmul_vv(Inst):
    name = 'vsmul.vv'
    # vsmul.vv vd, vs2, vs1, vm 
    # vd[i] = clip(roundoff_signed(vs2[i]*vs1[i], SEW-1))
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        shift  = self['sew']-1
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 

        tmp = np.array([0], dtype='object')   
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if (self['vs1'][ii] == self['vs2'][ii]) and (self['vs1'][ii] == np.iinfo(self['vs2'].dtype).min):
                    result[ii] = np.iinfo(self['vs2'].dtype).max
                    print('exit saturation: vs1 = '+str(self['vs1'][ii])+ '  vs2 = '+str(self['vs2'][ii]))
                    continue
                tmp[0] = np.multiply(self['vs2'][ii],self['vs1'][ii],dtype='object')
                result[ii] = self.rounding_xrm( tmp[0], vxrm, shift )               
        return result 


class Vsmul_vx(Inst):
    name = 'vsmul.vx'
    # vsmul.vx vd, vs2, rs1, vm 
    # vd[i] = clip(roundoff_signed(vs2[i]*x[rs1], SEW-1))
    def golden(self):
        if self['vl']==0:
            return self['ori']

        result = self['ori'].copy() 
        shift  = self['sew']-1
        vxrm   = self['vxrm'] if 'vxrm' in self else 0  
        vstart = self['vstart'] if 'vstart' in self else 0
        maskflag = 1 if 'mask' in self else 0 

        tmp = np.array([0], dtype='object')   
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                if (self['rs1'] == self['vs2'][ii]) and (self['rs1'] == np.iinfo(self['vs2'].dtype).min):
                    result[ii] = np.iinfo(self['vs2'].dtype).max
                    print('exit saturation: rs1 = '+str(self['rs1'])+ '  vs2 = '+str(self['vs2'][ii]))
                    continue
                tmp[0] = np.multiply(self['vs2'][ii],self['rs1'],dtype='object')
                result[ii] = self.rounding_xrm( tmp[0], vxrm, shift )               
        return result 
 
