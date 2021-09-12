from ...isa.inst import *
import numpy as np

class Vnsra_wv(Inst):
    name = 'vnsra.wv'
    # vnsra.wv vd, vs2, vs1, vm  
    def golden(self):  
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        if self['vs2'].dtype == self['vs1'].dtype: 
            self['vs1'].dtype = self.intdtype()
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) >> (self['vs1'][ii]%self['sew2']) 
        return result

class Vnsrl_wv(Vnsra_wv):
    name = 'vnsrl.wv'

