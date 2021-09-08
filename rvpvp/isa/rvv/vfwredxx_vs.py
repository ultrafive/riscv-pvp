from ...isa.inst import *
import numpy as np

import ctypes
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')
round_dict = { 0:FE_TONEAREST , 1:FE_TOWARDZERO , 2:FE_DOWNWARD , 3:FE_UPWARD  }

class Vfwredosum_vs(Inst):
    name = 'vfwredosum.vs'

    def golden(self):

        if 'vs1' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( 1, self['vs1'].dtype )

            if self['vl'] == 0:
                return result                

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0

            if 'mask' in self:
                mask = np.unpackbits( self['mask'], bitorder='little' )[vstart:self['vl']]
                mask = 1- mask
            else:
                mask = np.zeros( self['vl'] - vstart, dtype=np.uint8 )

            if mask.all() == True:
                result[0] = self['vs1'][0]
            else:
                result[0] = self['vs1'][0]
                vs2 = self['vs2'].astype(self['vs1'].dtype)
                for no in range( vstart, self['vl'] ):
                    if mask[no-vstart] == 0:
                        result[0] = result[0] + vs2[no]
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0

class Vfwredusum_vs(Vfwredosum_vs):
    name = 'vfwredsum.vs'      
