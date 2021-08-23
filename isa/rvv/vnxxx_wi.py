from isa.inst import *
import numpy as np

class Vnsra_wi(Inst):
    name = 'vnsra.wi'
    # vnsra.wi vd, vs2, uimm, vm    
    def golden(self):  
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) >> (self['uimm']%self['sew2']) 
        return result

class Vnsrl_wi(Vnsra_wi):
    name = 'vnsrl.wi'

