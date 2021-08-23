from isa.inst import *
import numpy as np

class Vwmacc_vv(Inst):
    name = 'vwmacc.vv'
    # vwmacc.vv vd, vs1, vs2, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) * self['vs1'][ii]+ self['ori'][ii].astype(object)
        return result 

class Vwmaccu_vv(Vwmacc_vv):
    name = 'vwmaccu.vv'

class Vwmaccsu_vv(Vwmacc_vv):
    name = 'vwmaccsu.vv'
