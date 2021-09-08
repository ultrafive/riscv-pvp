from ...isa.inst import *
import numpy as np

class Vzext_vf2(Inst):
    name = 'vzext.vf2'
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        maskflag = 1 if 'mask' in self else 0 
        vstart   = self['vstart'] if 'vstart' in self else 0 
        for ii in range(vstart, self['vl']): 
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                result[ii] = self['vs2'][ii]
        return result 

class Vzext_vf4(Vzext_vf2):
    name = 'vzext.vf4'

class Vzext_vf8(Vzext_vf2):
    name = 'vzext.vf8'

class Vsext_vf2(Vzext_vf2):
    name = 'vsext.vf2'

class Vsext_vf4(Vzext_vf2):
    name = 'vsext.vf4'

class Vsext_vf8(Vzext_vf2):
    name = 'vsext.vf8'
