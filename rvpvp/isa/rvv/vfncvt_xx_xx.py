from ...isa.inst import *
import numpy as np
import math

import ctypes
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')
round_dict = { 0:FE_TONEAREST , 1:FE_TOWARDZERO , 2:FE_DOWNWARD , 3:FE_UPWARD  }

class Vfncvt_xu_f_w(Inst):
    name = 'vfncvt.xu.f.w'
    type_dict = { 8:np.uint8, 16:np.uint16, 32:np.uint32 }
    max_dict = { 8:255, 16:65535, 32:4294967295 }

    def convert( self, a ):
        b = np.where( a < 0, 0, a )
        target_dtype = Vfncvt_xu_f_w.type_dict[self['ebits']]        

        if 'frm' in self:
            frm = self['frm']
        else:
            frm = 4

        if frm == 0:
            #rne
            b = np.rint( b )
            b = b.astype( target_dtype )
        elif frm == 1:
            #rtz
            b = np.trunc( b )
            b = b.astype( target_dtype )
        elif frm == 2:
            #rdn
            b = np.floor( b )
            b = b.astype( target_dtype )
        elif frm == 3:
            #rup
            b = np.ceil( b )
            b = b.astype( target_dtype )
        elif frm == 4:
            #rmm
            b = np.where( b - np.trunc( b ) == 0.5, b + 0.3, b )
            b = np.rint( b )
            b = b.astype( target_dtype )

        b = np.where( np.isnan(a), Vfncvt_xu_f_w.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfncvt_xu_f_w.max_dict[self['ebits']], b )

        b = np.where( a > Vfncvt_xu_f_w.max_dict[self['ebits']], Vfncvt_xu_f_w.max_dict[self['ebits']], b )        

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfncvt_xu_f_w.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self.convert( self['vs2'][vstart:self['vl']] ),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0

class Vfncvt_x_f_w(Inst):
    name = 'vfncvt.x.f.w'
    type_dict = { 8:np.int8, 16:np.int16, 32:np.int32 }
    max_dict = { 8:127, 16:32767, 32:2147483647 }
    min_dict = { 8:-128, 16:-32768, 32:-2147483648 }

    def convert( self, a ):
        b = a
        target_dtype = Vfncvt_x_f_w.type_dict[self['ebits']]        

        if 'frm' in self:
            frm = self['frm']
        else:
            frm = 4

        if frm == 0:
            #rne
            b = np.rint( b )
            b = b.astype( target_dtype )
        elif frm == 1:
            #rtz
            b = np.trunc( b )
            b = b.astype( target_dtype )
        elif frm == 2:
            #rdn
            b = np.floor( b )
            b = b.astype( target_dtype )
        elif frm == 3:
            #rup
            b = np.ceil( b )
            b = b.astype( target_dtype )
        elif frm == 4:
            #rmm
            b = np.where( b - np.trunc( b ) == 0.5, b + 0.3, b )
            b = np.where( b - np.trunc( b ) == -0.5, b -0.5, b )
            b = np.rint( b )
            b = b.astype( target_dtype )

        b = np.where( np.isnan(a), Vfncvt_x_f_w.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfncvt_x_f_w.max_dict[self['ebits']], b )

        b = np.where( np.isneginf(a), Vfncvt_x_f_w.min_dict[self['ebits']], b )

        b = np.where( a > Vfncvt_x_f_w.max_dict[self['ebits']], Vfncvt_x_f_w.max_dict[self['ebits']], b ) 
        b = np.where( a < Vfncvt_x_f_w.min_dict[self['ebits']], Vfncvt_x_f_w.min_dict[self['ebits']], b )       

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfncvt_x_f_w.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self.convert( self['vs2'][vstart:self['vl']] ),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0

class Vfncvt_rtz_xu_f_w(Inst):
    name = 'vfncvt.rtz.xu.f.w'
    type_dict = { 8:np.uint8, 16:np.uint16, 32:np.uint32 }
    max_dict = { 8:255, 16:65535, 32:4294967295 }

    def convert( self, a ):
        b = np.where( a < 0, 0, a )
        target_dtype = Vfncvt_rtz_xu_f_w.type_dict[self['ebits']]        

        #rtz
        b = np.trunc( b )
        b = b.astype( target_dtype )


        b = np.where( np.isnan(a), Vfncvt_rtz_xu_f_w.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfncvt_rtz_xu_f_w.max_dict[self['ebits']], b )

        b = np.where( a > Vfncvt_rtz_xu_f_w.max_dict[self['ebits']], Vfncvt_rtz_xu_f_w.max_dict[self['ebits']], b )        

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfncvt_rtz_xu_f_w.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self.convert( self['vs2'][vstart:self['vl']] ),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0

class Vfncvt_rtz_x_f_w(Inst):
    name = 'vfncvt.rtz.x.f.w'
    type_dict = { 8:np.int8, 16:np.int16, 32:np.int32 }
    max_dict = { 8:127, 16:32767, 32:2147483647 }
    min_dict = { 8:-128, 16:-32768, 32:-2147483648 }

    def convert( self, a ):
        b = a
        target_dtype = Vfncvt_rtz_x_f_w.type_dict[self['ebits']]        

        #rtz
        b = np.trunc( b )
        b = b.astype( target_dtype )


        b = np.where( np.isnan(a), Vfncvt_rtz_x_f_w.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfncvt_rtz_x_f_w.max_dict[self['ebits']], b )

        b = np.where( np.isneginf(a), Vfncvt_rtz_x_f_w.min_dict[self['ebits']], b )

        b = np.where( a > Vfncvt_rtz_x_f_w.max_dict[self['ebits']], Vfncvt_rtz_x_f_w.max_dict[self['ebits']], b ) 
        b = np.where( a < Vfncvt_rtz_x_f_w.min_dict[self['ebits']], Vfncvt_rtz_x_f_w.min_dict[self['ebits']], b )       

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfncvt_rtz_x_f_w.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self.convert( self['vs2'][vstart:self['vl']] ),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0

class Vfncvt_f_xu_w(Inst):
    name = 'vfncvt.f.xu.w'
    type_dict = { 16:np.float16, 32:np.float32 }

    def golden(self):
        if 'vs2' in self:
            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']])              

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfncvt_f_xu_w.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self['vs2'][vstart:self['vl']].astype(Vfncvt_f_xu_w.type_dict[self['ebits']]),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )   
                if ( self['frm'] == 1 or self['frm'] == 3 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isneginf( result[vstart:self['vl']] ), -65504, result[vstart:self['vl']] )    
                                 
                libm.fesetround( 0 )               

            return result
        else:
            return 0


class Vfncvt_f_x_w(Inst):
    name = 'vfncvt.f.x.w'
    type_dict = { 16:np.float16, 32:np.float32 }

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfncvt_f_x_w.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self['vs2'][vstart:self['vl']].astype(Vfncvt_f_x_w.type_dict[self['ebits']]),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0  




class Vfncvt_f_f_w(Inst):
    name = 'vfncvt.f.f.w'
    type_dict = { 16:np.float16, 32:np.float32 }

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfncvt_f_f_w.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self['vs2'][vstart:self['vl']].astype(Vfncvt_f_f_w.type_dict[self['ebits']]),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0            

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
    type_dict = { 16:np.float16, 32:np.float32 }

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfncvt_rod_f_f_w.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0 

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

            result[ vstart: self['vl'] ] = self.masked( vd[vstart:self['vl']],
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0

