from ...isa.inst import *
import numpy as np

class Vwadd_vx(Inst):
    name = 'vwadd.vx'
    # vwadd.vx vd, vs2, rs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) + self['rs1']
        return result 

class Vwaddu_vx(Vwadd_vx):
    name = 'vwaddu.vx'


class Vwsub_vx(Inst):
    name = 'vwsub.vx'
    # vwsub.vx vd, vs2, vs1, vm 
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) - self['rs1']
        return result 

class Vwsubu_vx(Vwsub_vx):
    name = 'vwsubu.vx'


class Vwmul_vx(Inst):
    name = 'vwmul.vx'
    # vwmul.vx vd, vs2, vs1, vm  
    def golden(self):
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) * self['rs1']
        return result 

class Vwmulu_vx(Vwmul_vx):
    name = 'vwmulu.vx'

class Vwmulsu_vx(Vwmul_vx):
    name = 'vwmulsu.vx'

