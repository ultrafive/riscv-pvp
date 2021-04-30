from isa.inst import *
import numpy as np
import math

def f32_to_f16( x ):
    num = int( np.array( [x], dtype=np.float32 ).byteswap().tobytes().hex(), 16 )
    sign = num >> 31
    exp = ( num >> 23 ) & 0xFF  
    frac = num & 0x7FFFFF 
    if exp == 0xFF:
        if frac: #nan
            res = np.array([0x7E00]).astype(np.int16)
            res.dtype = np.float16
            return res[0]
        else: #inf
            res = ( sign << 15 ) + ( 0x1F << 10 ) + 0
            res = np.array([res]).astype(np.int16)
            res.dtype = np.float16
            return res[0]
    
    frac16 = ( frac >> 9 ) | (( frac & 0x1FF ) != 0 ) 
    if not ( exp | frac16 ):
        res = sign << 15
        res = np.array([res]).astype(np.int16)
        res.dtype = np.float16
        return res[0] 

    exp = exp - 0x71
    frac16 = frac16 | 0x4000

    if exp < 0:
        if (-exp) < 31:
            frac16 = ( frac16 >> ( -exp ) ) | ((frac16 & ( ( 1 << (-exp) )- 1 ) ) != 0 )
        else:
            frac16 = ( frac16 != 0 )
        exp = 0
    
    elif exp > 0x1D:
        res = ( sign << 15 ) + ( 0x1F << 10 ) + 0 - 1
        res = np.array([res]).astype(np.int16)
        res.dtype = np.float16
        return res[0]

    roundbits = frac16 & 0xF
    frac16 = frac16 >> 4
    if roundbits:
        frac16 = frac16 | 1
    if not frac16:
        exp = 0

    res = ( sign << 15 ) + ( exp << 10 ) + frac16
    res = np.array([res]).astype(np.int16)
    res.dtype = np.float16
    return res[0]    

def f64_to_f32( x ):
    num = int( np.array( [x], dtype=np.float64 ).byteswap().tobytes().hex(), 16 )
    sign = num >> 63
    exp = ( num >> 52 ) & 0x7FF  
    frac = num & 0xFFFFFFFFFFFFF 
    if exp == 0x7FF:
        if frac: #nan
            res = np.array([0x7FC00000]).astype(np.int32)
            res.dtype = np.float32
            return res[0]
        else: #inf
            res = ( sign << 31 ) + ( 0xFF << 23 ) + 0
            res = np.array([res]).astype(np.int32)
            res.dtype = np.float32
            return res[0]
    
    frac32 = ( frac >> 22 ) | (( frac & ( ( 1 << 22 ) - 1 ) ) != 0 ) 
    if not ( exp | frac32 ):
        res = sign << 31
        res = np.array([res]).astype(np.int32)
        res.dtype = np.float32
        return res[0] 

    exp = exp - 0x381
    frac32 = frac32 | 0x40000000

    if exp < 0:
        if (-exp) < 31:
            frac32 = ( frac32 >> ( -exp ) ) | ((frac32 & ( ( 1 << (-exp) )- 1 ) ) != 0 )
        else:
            frac32 = ( frac32 != 0 )
        exp = 0
    
    elif exp > 0xFD:
        res = ( sign << 31 ) + ( 0xFF << 23 ) + 0 - 1
        res = np.array([res]).astype(np.int32)
        res.dtype = np.float32
        return res[0]

    roundbits = frac32 & 0x7F
    frac32 = frac32 >> 7
    if roundbits:
        frac32 = frac32 | 1
    if not frac32:
        exp = 0

    res = ( sign << 31 ) + ( exp << 23 ) + frac32
    res = np.array([res]).astype(np.int32)
    res.dtype = np.float32
    return res[0] 






    


class Vfncvt_rod_f_f_w(Inst):
    name = 'vfncvt.rod.f.f.w'

    def golden(self):

        if self['vs2'].dtype == np.float32:
            vd = self['vs2'].astype( np.float16 ) 
            for no in range( vd.size ):
                num = f32_to_f16( self['vs2'][no] )                
                vd[no] = num

        elif self['vs2'].dtype == np.float64:
            vd = self['vs2'].astype( np.float32 ) 
            for no in range( vd.size ):
                num = f64_to_f32( self['vs2'][no] )                
                vd[no] = num

        # vd = self['vs2'].astype( target_dtype )
        # vd = np.where( np.isposinf( vd ), np.finfo( vd.dtype ).max, vd )
        # vd = np.where( np.isneginf( vd ), np.finfo( vd.dtype ).min, vd )


        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd