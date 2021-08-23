from isa.inst import *
import numpy as np

class Vnsra_wx(Inst):
    name = 'vnsra.wx'
    # vnsra.wx vd, vs2, rs1, vm    
    def golden(self):  
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) >> (self['rs1']%self['sew2']) 
        return result

class Vnsrl_wx(Vnsra_wx):
    name = 'vnsrl.wx'

