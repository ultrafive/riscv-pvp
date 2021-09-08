from ...isa.inst import *
import numpy as np

import ctypes
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')
round_dict = { 0:FE_TONEAREST , 1:FE_TOWARDZERO , 2:FE_DOWNWARD , 3:FE_UPWARD  }

class Vfredosum_vs(Inst):
    name = 'vfredosum.vs'

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
                for no in range( vstart, self['vl'] ):
                    if mask[no-vstart] == 0:
                        result[0] = result[0] + self['vs2'][no]
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0

class Vfredusum_vs(Vfredosum_vs):
    name = 'vfredsum.vs'


class Vfredmax_vs(Inst):
    name = 'vfredmax.vs'

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
                vs1= np.ma.array(self['vs1'].copy())
                vs2 = np.ma.array( self['vs2'][vstart:self['vl']], mask=mask )
                vs = np.ma.concatenate([vs1, vs2])
                vs_nan = np.ma.where( np.isnan(vs), 1, 0 )
                if vs_nan.any() == True and not vs_nan.all() == True:
                    vs = np.ma.where( vs_nan==1, np.NINF, vs )
                
                result[0] = vs.max()
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0

class Vfredmin_vs(Inst):
    name = 'vfredmin.vs'

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
                vs1= np.ma.array(self['vs1'].copy())
                vs2 = np.ma.array( self['vs2'][vstart:self['vl']], mask=mask )
                vs = np.ma.concatenate([vs1, vs2])
                vs_nan = np.ma.where( np.isnan(vs), 1, 0 )
                if vs_nan.any() == True and not vs_nan.all() == True:
                    vs = np.ma.where( vs_nan==1, np.PINF, vs )
                
                result[0] = vs.min()
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0      

