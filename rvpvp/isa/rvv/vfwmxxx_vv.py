from ...isa.inst import *
import numpy as np

import ctypes
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')
round_dict = { 0:FE_TONEAREST , 1:FE_TOWARDZERO , 2:FE_DOWNWARD , 3:FE_UPWARD  }
INF_dict = {0: np.PINF, 1: np.NINF}


def muladd( a, b, c, l ):

    result = np.zeros( l, dtype=a.dtype )

    for no in range(0, l):
        signProd = ( a[no] < 0 ) ^ ( b[no] < 0 )
        if np.isnan( a[no] ) or np.isnan( b[no] ):
            result[no] = np.nan
        elif ( np.isinf(a[no]) and b[no] == 0 ) or ( a[no] == 0 and np.isinf(b[no]) ):
            result[no] = np.nan
        elif np.isinf(a[no] ) or np.isinf(b[no]):
            if not np.isnan( c[no] ) and not np.isinf( c[no] ):
                result[no] = INF_dict[signProd]
            elif np.isnan( c[no] ):
                result[no] = np.nan
            elif ( c[no] < 0 ) == signProd:
                result[no] = INF_dict[signProd]
            else:
                result[no] = np.nan
        elif np.isnan( c[no] ):
            result[no] = np.nan
        elif np.isinf( c[no] ):
            result[no] = c[no]
        else:
            result[no] = ( a[no].astype(np.float64) * b[no].astype(np.float64) + c[no]  ).astype(result.dtype)
    
    return result 

class Vfwmacc_vv(Inst):
    name = 'vfwmacc.vv'

    def golden(self):
        if 'vs1' in self:

            dtype_vs = self['vs1'].dtype
            if dtype_vs == np.float16:
                dtype_vd = np.float32
            elif dtype_vs == np.float32:
                dtype_vd = np.float64 

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = self['vd'].copy()

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0
            
            value = muladd( self['vs1'][vstart:self['vl']].astype( dtype_vd ), self['vs2'][vstart:self['vl']].astype( dtype_vd ), result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )


            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0 

class Vfwnmacc_vv(Inst):
    name = 'vfwnmacc.vv'

    def golden(self):
        if 'vs1' in self:

            dtype_vs = self['vs1'].dtype
            if dtype_vs == np.float16:
                dtype_vd = np.float32
            elif dtype_vs == np.float32:
                dtype_vd = np.float64 

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = self['vd'].copy()

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0
            
            value = muladd( - self['vs1'][vstart:self['vl']].astype( dtype_vd ), self['vs2'][vstart:self['vl']].astype( dtype_vd ), - result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )


            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0           

class Vfwmsac_vv(Inst):
    name = 'vfwmsac.vv'

    def golden(self):
        if 'vs1' in self:

            dtype_vs = self['vs1'].dtype
            if dtype_vs == np.float16:
                dtype_vd = np.float32
            elif dtype_vs == np.float32:
                dtype_vd = np.float64 

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = self['vd'].copy()

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0
            
            value = muladd( self['vs1'][vstart:self['vl']].astype( dtype_vd ), self['vs2'][vstart:self['vl']].astype( dtype_vd ), - result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )


            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0         

class Vfwnmsac_vv(Inst):
    name = 'vfwnmsac.vv'

    def golden(self):
        if 'vs1' in self:

            dtype_vs = self['vs1'].dtype
            if dtype_vs == np.float16:
                dtype_vd = np.float32
            elif dtype_vs == np.float32:
                dtype_vd = np.float64 

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = self['vd'].copy()

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0
            
            value = muladd( - self['vs1'][vstart:self['vl']].astype( dtype_vd ), self['vs2'][vstart:self['vl']].astype( dtype_vd ), result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )


            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0                                          
