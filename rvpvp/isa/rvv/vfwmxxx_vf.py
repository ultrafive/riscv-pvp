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
        signProd = ( a[0] < 0 ) ^ ( b[no] < 0 )
        if np.isnan( a[0] ) or np.isnan( b[no] ):
            result[no] = np.nan
        elif ( np.isinf(a[0]) and b[no] == 0 ) or ( a[0] == 0 and np.isinf(b[no]) ):
            result[no] = np.nan
        elif np.isinf(a[0] ) or np.isinf(b[no]):
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
            result[no] = ( a[0].astype(np.float64) * b[no].astype(np.float64) + c[no]  ).astype(result.dtype)
    
    return result  

class Vfwmacc_vf(Inst):
    name = 'vfwmacc.vf'

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
                result = self['vd'].copy()

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0
            
            value = muladd( self['rs1'].astype( dtype_vd ), self['vs2'][vstart:self['vl']].astype( dtype_vd ), result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )


            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0        
    

class Vfwnmacc_vf(Inst):
    name = 'vfwnmacc.vf'

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
                result = self['vd'].copy()

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0
            
            value = muladd( - self['rs1'].astype( dtype_vd ), self['vs2'][vstart:self['vl']].astype( dtype_vd ), - result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )


            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0                  


class Vfwmsac_vf(Inst):
    name = 'vfwmsac.vf'

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
                result = self['vd'].copy()

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0
            
            value = muladd( self['rs1'].astype( dtype_vd ), self['vs2'][vstart:self['vl']].astype( dtype_vd ), - result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )


            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0


class Vfwnmsac_vf(Inst):
    name = 'vfwnmsac.vf'

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
                result = self['vd'].copy()

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0
            
            value = muladd( - self['rs1'].astype( dtype_vd ), self['vs2'][vstart:self['vl']].astype( dtype_vd ), result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )


            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0        

