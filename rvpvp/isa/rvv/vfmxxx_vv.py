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

class Vfmacc_vv(Inst):
    name = 'vfmacc.vv'

    def golden(self):
        if 'vs1' in self:

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
            
            value = muladd( self['vs1'][vstart:self['vl']], self['vs2'][vstart:self['vl']], result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )


            
            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] ) 

                libm.fesetround( 0 )        

            return result
        else:
            return 0


class Vfnmacc_vv(Inst):
    name = 'vfnmacc.vv'

    def golden(self):
        if 'vs1' in self:

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

            value = muladd( self['vs1'][vstart:self['vl']], - self['vs2'][vstart:self['vl']], - result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] ) 

                libm.fesetround( 0 )        

            return result
        else:
            return 0



class Vfmsac_vv(Inst):
    name = 'vfmsac.vv'

    def golden(self):
        if 'vs1' in self:

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


            value = muladd( self['vs1'][vstart:self['vl']], self['vs2'][vstart:self['vl']], - result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )

            
            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] ) 

                libm.fesetround( 0 )        

            return result
        else:
            return 0        


class Vfnmsac_vv(Inst):
    name = 'vfnmsac.vv'

    def golden(self):
        if 'vs1' in self:

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


            value = muladd( self['vs1'][vstart:self['vl']], - self['vs2'][vstart:self['vl']], result[vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] ) 

                libm.fesetround( 0 )        

            return result
        else:
            return 0        

class Vfmadd_vv(Inst):
    name = 'vfmadd.vv'

    def golden(self):
        if 'vs1' in self:

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


            value = muladd( self['vs1'][vstart:self['vl']], result[vstart:self['vl']], self['vs2'][vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] ) 

                libm.fesetround( 0 )        

            return result
        else:
            return 0        

class Vfnmadd_vv(Inst):
    name = 'vfnmadd.vv'

    def golden(self):
        if 'vs1' in self:

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


            value = muladd( self['vs1'][vstart:self['vl']], - result[vstart:self['vl']], - self['vs2'][vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] ) 

                libm.fesetround( 0 )        

            return result
        else:
            return 0         


class Vfmsub_vv(Inst):
    name = 'vfmsub.vv'

    def golden(self):
        if 'vs1' in self:

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


            value = muladd( self['vs1'][vstart:self['vl']], result[vstart:self['vl']], - self['vs2'][vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] )                 
                libm.fesetround( 0 )        

            return result
        else:
            return 0         
 

class Vfnmsub_vv(Inst):
    name = 'vfnmsub.vv'

    def golden(self):
        if 'vs1' in self:

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


            value = muladd( self['vs1'][vstart:self['vl']], - result[vstart:self['vl']], self['vs2'][vstart:self['vl']], self['vl'] - vstart )

            result[vstart:self['vl']] = self.masked( value, result[vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] )    
                                 
                libm.fesetround( 0 )        

            return result
        else:
            return 0         

