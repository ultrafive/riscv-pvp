from isa.inst import *
import numpy as np

class Vwadd_vv(Inst):
    name = 'vwadd.vv'
    # vwadd.vv vd, vs2, vs1, vm 
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]+self['vs1'][ii].astype(object)
        return result 

class Vwaddu_vv(Vwadd_vv):
    name = 'vwaddu.vv'


class Vwsub_vv(Inst):
    name = 'vwsub.vv'
    # vwsub.vv vd, vs2, vs1, vm 
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]-self['vs1'][ii].astype(object)
        return result 

class Vwsubu_vv(Vwsub_vv):
    name = 'vwsubu.vv'


class Vwmul_vv(Inst):
    name = 'vwmul.vv'
    # vwmul.vv vd, vs2, vs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]*self['vs1'][ii].astype(object)
        return result 


class Vwmulu_vv(Vwmul_vv):
    name = 'vwmulu.vv'

class Vwmulsu_vv(Vwmul_vv):
    name = 'vwmulsu.vv'
