from isa.inst import *
import numpy as np

class Vmacc_vx(Inst):
    name = 'vmacc.vx'
    # vmacc.vx vd, rs1, vs2, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]* self['rs1']+ self['ori'][ii]  #.astype(object) 
        return result 


class Vnmsac_vx(Inst):
    name = 'vnmsac.vx'
    # vnmsac.vx vd, rs1, vs2, vm   
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = -(self['vs2'][ii] * self['rs1']) + self['ori'][ii]
        return result 


class Vmadd_vx(Inst):
    name = 'vmadd.vx'
    # vmadd.vx vd, rs1, vs2, vm    
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['rs1']* self['ori'][ii] + self['vs2'][ii]
        return result 


class Vnmsub_vx(Inst):
    name = 'vnmsub.vx'
    # vnmsub.vx vd, rs1, vs2, vm   
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = -(self['rs1'] * self['ori'][ii]) + self['vs2'][ii]
        return result 

