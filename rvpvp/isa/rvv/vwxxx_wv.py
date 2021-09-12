from ...isa.inst import *
import numpy as np

class Vwadd_wv(Inst):
    name = 'vwadd.wv'
    # vwadd.wv vd, vs2, vs1, vm 
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
                result[ii] = self['vs2'][ii].astype(object) + self['vs1'][ii]#.astype(intdtype(self['sew'])) 
        return result 

class Vwaddu_wv(Vwadd_wv):
    name = 'vwaddu.wv'


class Vwsub_wv(Inst):
    name = 'vwsub.wv'
    # vwsub.wv vd, vs2, vs1, vm 
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        if self['vs2'].dtype == self['vs1'].dtype:
            self['vs1'].dtype = self.uintdtype()
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) - self['vs1'][ii]
        return result 

class Vwsubu_wv(Vwsub_wv):
    name = 'vwsubu.wv'
