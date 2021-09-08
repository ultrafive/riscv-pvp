from ...isa.inst import *
import numpy as np

import ctypes
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')
round_dict = { 0:FE_TONEAREST , 1:FE_TOWARDZERO , 2:FE_DOWNWARD , 3:FE_UPWARD  }

class Vfwadd_vf(Inst):
    name = 'vfwadd.vf'

    def golden(self):
        if 'vs2' in self:

            dtype_vs = self['vs2'].dtype
            if dtype_vs == np.float16:
                dtype_vd = np.float32
            elif dtype_vs == np.float32:
                dtype_vd = np.float64            

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = dtype_vd )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'].astype( dtype_vd )[vstart:self['vl']] + 
            self['rs1'].astype( dtype_vd ), self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0



class Vfwsub_vf(Inst):
    name = 'vfwsub.vf'

    def golden(self):
        if 'vs2' in self:

            dtype_vs = self['vs2'].dtype
            if dtype_vs == np.float16:
                dtype_vd = np.float32
            elif dtype_vs == np.float32:
                dtype_vd = np.float64            

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = dtype_vd )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'].astype( dtype_vd )[vstart:self['vl']] - 
            self['rs1'].astype( dtype_vd ), self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0

class Vfwmul_vf(Inst):
    name = 'vfwmul.vf'

    def golden(self):
        if 'vs2' in self:

            dtype_vs = self['vs2'].dtype
            if dtype_vs == np.float16:
                dtype_vd = np.float32
            elif dtype_vs == np.float32:
                dtype_vd = np.float64            

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = dtype_vd )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['vs2'].astype( dtype_vd )[vstart:self['vl']] * 
            self['rs1'].astype( dtype_vd ), self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0

