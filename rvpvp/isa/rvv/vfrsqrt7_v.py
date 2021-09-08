from ...isa.inst import *
import numpy as np

def f16_classify( vs2 ):

    num = int( np.array( [vs2], dtype = np.float16 ).byteswap().tobytes().hex(), 16 )
    
    infOrNaN = ( ( num >> 10 ) & 0x1F ) == 0x1F
    subnormalOrZero = ( ( num >> 10 ) & 0x1F ) == 0
    sign = ( ( num >> 15 ) != 0 )
    fracZero = ( num & 0x3FF ) == 0
    isNaN = ( ( ( ~ num ) & 0x7C00 ) == 0 ) and ( ( num & 0x03FF ) != 0)
    isSNaN =  ( ( num & 0x7E00 ) == 0x7C00 ) and ( ( num & 0x1FF ) != 0 )
    vd = ( 
    (  sign and infOrNaN and fracZero ) << 0 | 
    (  sign and not infOrNaN and not subnormalOrZero ) << 1 |
    (  sign and subnormalOrZero and not fracZero )  << 2 |
    (  sign and subnormalOrZero and fracZero )   << 3 |
    ( not sign and subnormalOrZero and fracZero )   << 4 | 
    ( not sign and subnormalOrZero and not fracZero )  << 5 |
    ( not sign and not infOrNaN and not subnormalOrZero ) << 6 |                      
    ( not sign and infOrNaN and fracZero )          << 7 |
    ( isNaN and  isSNaN )                       << 8 |
    ( isNaN and not isSNaN )                       << 9  )

    return vd

def f32_classify( vs2 ):

    num = int( np.array( [vs2], dtype = np.float32 ).byteswap().tobytes().hex(), 16 )
    
    infOrNaN = ( ( num >> 23 ) & 0xFF ) == 0xFF
    subnormalOrZero = ( ( num >> 23 ) & 0xFF ) == 0
    sign = ( ( num >> 31 ) != 0 )
    fracZero = ( num & 0x7FFFFF ) == 0
    isNaN = ( ( ( ~ num ) & 0x7F800000) == 0) and ( ( num & 0x007FFFFF) != 0 )
    isSNaN =  ( ( num & 0x7FC00000 ) == 0x7F800000 ) and ( ( num & 0x3FFFFF ) != 0 )
    vd = ( 
    (  sign and infOrNaN and fracZero ) << 0 | 
    (  sign and not infOrNaN and not subnormalOrZero ) << 1 |
    (  sign and subnormalOrZero and not fracZero )  << 2 |
    (  sign and subnormalOrZero and fracZero )   << 3 |
    ( not sign and subnormalOrZero and fracZero )   << 4 | 
    ( not sign and subnormalOrZero and not fracZero )  << 5 |
    ( not sign and not infOrNaN and not subnormalOrZero ) << 6 |                      
    ( not sign and infOrNaN and fracZero )          << 7 |
    ( isNaN and  isSNaN )                       << 8 |
    ( isNaN and not isSNaN )                       << 9  )

    return vd

def f64_classify( vs2 ):

    num = int( np.array( [vs2], dtype = np.float64 ).byteswap().tobytes().hex(), 16 )

    infOrNaN = ( ( num >> 52 ) & 0x7FF ) == 0x7FF
    subnormalOrZero = ( ( num >> 52 ) & 0x7FF ) == 0
    sign = ( ( num >> 63 ) != 0 )
    fracZero = ( num & 0xFFFFFFFFFFFFF ) == 0
    isNaN = ( ( ( ~num ) & 0x7FF0000000000000 ) == 0) and ( ( num & 0x000FFFFFFFFFFFFF ) != 0 )
    isSNaN =  ( ( num & 0x7FF8000000000000 ) == 0x7FF0000000000000 ) and ( ( num & 0x7FFFFFFFFFFFF ) != 0 )
    vd = ( 
    (  sign and infOrNaN and fracZero ) << 0 | 
    (  sign and not infOrNaN and not subnormalOrZero ) << 1 |
    (  sign and subnormalOrZero and not fracZero )  << 2 |
    (  sign and subnormalOrZero and fracZero )   << 3 |
    ( not sign and subnormalOrZero and fracZero )   << 4 | 
    ( not sign and subnormalOrZero and not fracZero )  << 5 |
    ( not sign and not infOrNaN and not subnormalOrZero ) << 6 |                      
    ( not sign and infOrNaN and fracZero )          << 7 |
    ( isNaN and  isSNaN )                       << 8 |
    ( isNaN and not isSNaN )                       << 9  )

    return vd

rsqrt_table = [ 
    52, 51, 50, 48, 47, 46, 44, 43,
    42, 41, 40, 39, 38, 36, 35, 34,
    33, 32, 31, 30, 30, 29, 28, 27,
    26, 25, 24, 23, 23, 22, 21, 20,
    19, 19, 18, 17, 16, 16, 15, 14,
    14, 13, 12, 12, 11, 10, 10, 9,
    9, 8, 7, 7, 6, 6, 5, 4,
    4, 3, 3, 2, 2, 1, 1, 0,
    127, 125, 123, 121, 119, 118, 116, 114,
    113, 111, 109, 108, 106, 105, 103, 102,
    100, 99, 97, 96, 95, 93, 92, 91,
    90, 88, 87, 86, 85, 84, 83, 82,
    80, 79, 78, 77, 76, 75, 74, 73,
    72, 71, 70, 70, 69, 68, 67, 66,
    65, 64, 63, 63, 62, 61, 60, 59,
    59, 58, 57, 56, 56, 55, 54, 53 ]

def rsqrt7( num, num_exp, num_sig, IsSubnormal ):
    exp = ( num >> num_sig ) & ( ( 1 << num_exp ) - 1 )
    sig = num & ( ( 1 << num_sig ) - 1 )
    sign = num >> ( num_exp + num_sig )

    if IsSubnormal:
        while (sig & ( 1 << ( num_sig - 1 ) ) ) == 0:
            exp = exp - 1
            sig = sig << 1
        sig = ( sig << 1 ) & ( ( 1 << num_sig ) - 1 )
    
    index = ( ( exp & 1 ) << 6 ) | ( sig >> ( num_sig - 6 ) )
    out_sig = rsqrt_table[ index ] << ( num_sig - 7 )
    out_exp = int( np.floor( (3 * ((1 << (num_exp-1))-1) - 1 - exp)/2 ))

    return ( sign << (num_exp+num_sig) ) | ( out_exp << num_sig ) | out_sig


def f16_rsqrt7( vs2 ):
    vd = np.zeros( vs2.shape[0], dtype=vs2.dtype )
    
    for no in range(0, vs2.size ):
        IsSubnoraml = False
        res_class = f16_classify( vs2[no] )
        if res_class == 0x1 or res_class == 0x2 or res_class == 0x4 or res_class == 0x100 or res_class == 0x200:
            vd[no] = np.nan
            continue
        elif res_class == 0x8:
            vd[no] = np.NINF
            continue 
        elif res_class == 0x10:
            vd[no] = np.PINF
            continue
        elif res_class == 0x80:
            vd[no] = 0
            continue
        elif res_class == 0x20:
            IsSubnoraml = True
        
        num = int( np.array( [vs2[no]], dtype = np.float16 ).byteswap().tobytes().hex(), 16 )
        num = rsqrt7( num, 5, 10, IsSubnoraml )
        num = np.array([num]).astype(np.int16)
        num.dtype= np.float16       
        vd[no] = num[0]
    return vd

def f32_rsqrt7( vs2 ):
    vd = np.zeros( vs2.shape[0], dtype=vs2.dtype )
    
    for no in range(0, vs2.size ):
        IsSubnoraml = False
        res_class = f32_classify( vs2[no] )
        if res_class == 0x1 or res_class == 0x2 or res_class == 0x4 or res_class == 0x100 or res_class == 0x200:
            vd[no] = np.nan
            continue
        elif res_class == 0x8:
            vd[no] = np.NINF
            continue 
        elif res_class == 0x10:
            vd[no] = np.PINF
            continue
        elif res_class == 0x80:
            vd[no] = 0
            continue
        elif res_class == 0x20:
            IsSubnoraml = True
        
        num = int( np.array( [vs2[no]], dtype = np.float32 ).byteswap().tobytes().hex(), 16 )
        num = rsqrt7( num, 8, 23, IsSubnoraml )
        num = np.array([num]).astype(np.int32)
        num.dtype= np.float32
        vd[no] = num[0]
    return vd        

def f64_rsqrt7( vs2 ):
    vd = np.zeros( vs2.shape[0], dtype=vs2.dtype )
    
    for no in range(0, vs2.size ):
        IsSubnoraml = False
        res_class = f64_classify( vs2[no] )
        if res_class == 0x1 or res_class == 0x2 or res_class == 0x4 or res_class == 0x100 or res_class == 0x200:
            vd[no] = np.nan
            continue
        elif res_class == 0x8:
            vd[no] = np.NINF
            continue 
        elif res_class == 0x10:
            vd[no] = np.PINF
            continue
        elif res_class == 0x80:
            vd[no] = 0
            continue
        elif res_class == 0x20:
            IsSubnoraml = True
        
        num = int( np.array( [vs2[no]], dtype = np.float64 ).byteswap().tobytes().hex(), 16 )
        num = rsqrt7( num, 11, 52, IsSubnoraml )
        num = np.array([num]).astype(np.int64)
        num.dtype= np.float64      
        vd[no] = num[0] 
    return vd   

import ctypes
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')
round_dict = { 0:FE_TONEAREST , 1:FE_TOWARDZERO , 2:FE_DOWNWARD , 3:FE_UPWARD  }

def f_rsqrt7( vs2 ):

    if vs2.dtype == np.float16:
        vd = f16_rsqrt7( vs2 )
    elif vs2.dtype == np.float32:
        vd = f32_rsqrt7( vs2 )
    elif vs2.dtype == np.float64:
        vd = f64_rsqrt7( vs2 )
    
    return vd

class Vfrsqrt7_v(Inst):
    name = 'vfrsqrt7.v'

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']]) 

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( f_rsqrt7( self['vs2'][vstart:self['vl']] ), self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            if 'frm' in self:
                libm.fesetround( 0 )        

            return result
        else:
            return 0

