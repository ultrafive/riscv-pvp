from ...isa.inst import *
import numpy as np

class Vwadd_wx(Inst):
    name = 'vwadd.wx'
    # vwadd.wx vd, vs2, rs1, vm  
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        print("vstart = "+str(vstart))
        print("vl     = "+str(self['vl']))
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii].astype(object) + self['rs1']
        return result 

class Vwaddu_wx(Vwadd_wx):
    name = 'vwaddu.wx'


class Vwsub_wx(Inst):
    name = 'vwsub.wx'
    # vwsub.wx vd, vs2, rs1, vm  
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

class Vwsubu_wx(Vwsub_wx):
    name = 'vwsubu.wx'

