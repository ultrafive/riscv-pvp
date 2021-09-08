from ...isa.inst import *
import numpy as np

class Vmacc_vv(Inst):
    name = 'vmacc.vv'
    # vmacc.vv vd, vs1, vs2, vm 
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) * self['vs1'][ii] + self['ori'][ii]
        return result 


class Vnmsac_vv(Inst):
    name = 'vnmsac.vv'
    # vnmsac.vv vd, vs1, vs2, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = -(self['vs2'][ii].astype(object) * self['vs1'][ii]) + self['ori'][ii]
        return result 


class Vmadd_vv(Inst):
    name = 'vmadd.vv'
    # vmadd.vv vd, vs1, vs2, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs1'][ii] * self['ori'][ii] + self['vs2'][ii]
        return result 


class Vnmsub_vv(Inst):
    name = 'vnmsub.vv'
    # vnmsub.vv vd, vs1, vs2, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = -(self['vs1'][ii].astype(object) * self['ori'][ii]) + self['vs2'][ii]
        return result 

