from ...isa.inst import *
import numpy as np

class Vwmacc_vx(Inst):
    name = 'vwmacc.vx'
    # vwmacc.vx vd, rs1, vs2, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) * self['rs1']+ self['ori'][ii].astype(object)
        return result 

class Vwmaccu_vx(Vwmacc_vx):
    name = 'vwmaccu.vx'

class Vwmaccsu_vx(Vwmacc_vx):
    name = 'vwmaccsu.vx'

class Vwmaccus_vx(Vwmacc_vx):
    name = 'vwmaccus.vx'
