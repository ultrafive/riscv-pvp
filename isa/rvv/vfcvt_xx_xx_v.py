from isa.inst import *
import numpy as np
import math

import ctypes
FE_TONEAREST = 0x0000
FE_DOWNWARD = 0x0400
FE_UPWARD = 0x0800
FE_TOWARDZERO = 0x0c00
libm = ctypes.CDLL('libm.so.6')
round_dict = { 0:FE_TONEAREST , 1:FE_TOWARDZERO , 2:FE_DOWNWARD , 3:FE_UPWARD  }

class Vfcvt_xu_f_v(Inst):
    name = 'vfcvt.xu.f.v'
    type_dict = { 16:np.uint16, 32:np.uint32, 64:np.uint64 }
    max_dict = { 16:65535, 32:4294967295, 64:18446744073709551615 }

    def convert( self, a ):
        b = np.where( a < 0, 0, a )
        target_dtype = Vfcvt_xu_f_v.type_dict[self['ebits']]        

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

        b = np.where( np.isnan(a), Vfcvt_xu_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfcvt_xu_f_v.max_dict[self['ebits']], b )

        b = np.where( a > Vfcvt_xu_f_v.max_dict[self['ebits']], Vfcvt_xu_f_v.max_dict[self['ebits']], b )        

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfcvt_xu_f_v.type_dict[self['ebits']] )

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

class Vfcvt_x_f_v(Inst):
    name = 'vfcvt.x.f.v'
    type_dict = { 16:np.int16, 32:np.int32, 64:np.int64 }
    max_dict = { 16:32767, 32:2147483647, 64:9223372036854775807 }
    min_dict = { 16:-32768, 32:-2147483648, 64:-9223372036854775808 }

    def convert( self, a ):
        b = a
        target_dtype = Vfcvt_x_f_v.type_dict[self['ebits']]        

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

        b = np.where( np.isnan(a), Vfcvt_x_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfcvt_x_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isneginf(a), Vfcvt_x_f_v.min_dict[self['ebits']], b )

        b = np.where( a > Vfcvt_x_f_v.max_dict[self['ebits']], Vfcvt_x_f_v.max_dict[self['ebits']], b ) 
        b = np.where( a < Vfcvt_x_f_v.min_dict[self['ebits']], Vfcvt_x_f_v.min_dict[self['ebits']], b )       

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfcvt_x_f_v.type_dict[self['ebits']] )

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

class Vfcvt_rtz_xu_f_v(Inst):
    name = 'vfcvt.rtz.xu.f.v'
    type_dict = { 16:np.uint16, 32:np.uint32, 64:np.uint64 }
    max_dict = { 16:65535, 32:4294967295, 64:18446744073709551615 }

    def convert( self, a ):
        b = np.where( a < 0, 0, a )
        target_dtype = Vfcvt_rtz_xu_f_v.type_dict[self['ebits']]        

        #rtz
        b = np.trunc( b )
        b = b.astype( target_dtype )


        b = np.where( np.isnan(a), Vfcvt_rtz_xu_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfcvt_rtz_xu_f_v.max_dict[self['ebits']], b )

        b = np.where( a > Vfcvt_rtz_xu_f_v.max_dict[self['ebits']], Vfcvt_rtz_xu_f_v.max_dict[self['ebits']], b )        

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfcvt_rtz_xu_f_v.type_dict[self['ebits']] )

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

class Vfcvt_rtz_x_f_v(Inst):
    name = 'vfcvt.rtz.x.f.v'
    type_dict = { 16:np.int16, 32:np.int32, 64:np.int64 }
    max_dict = { 16:32767, 32:2147483647, 64:9223372036854775807 }
    min_dict = { 16:-32768, 32:-2147483648, 64:-9223372036854775808 }

    def convert( self, a ):
        b = a
        target_dtype = Vfcvt_rtz_x_f_v.type_dict[self['ebits']]        

        #rtz
        b = np.trunc( b )
        b = b.astype( target_dtype )


        b = np.where( np.isnan(a), Vfcvt_rtz_x_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfcvt_rtz_x_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isneginf(a), Vfcvt_rtz_x_f_v.min_dict[self['ebits']], b )

        b = np.where( a > Vfcvt_rtz_x_f_v.max_dict[self['ebits']], Vfcvt_rtz_x_f_v.max_dict[self['ebits']], b ) 
        b = np.where( a < Vfcvt_rtz_x_f_v.min_dict[self['ebits']], Vfcvt_rtz_x_f_v.min_dict[self['ebits']], b )       

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfcvt_rtz_x_f_v.type_dict[self['ebits']] )

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

class Vfcvt_f_xu_v(Inst):
    name = 'vfcvt.f.xu.v'
    type_dict = { 16:np.float16, 32:np.float32, 64:np.float64 }

    def golden(self):
        if 'vs2' in self:

            if 'frm' in self:
                libm.fesetround(round_dict[self['frm']])             

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfcvt_f_xu_v.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self['vs2'][vstart:self['vl']].astype(Vfcvt_f_xu_v.type_dict[self['ebits']]),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            if 'frm' in self:
                if ( self['frm'] == 1 or self['frm'] == 2 )and result.dtype == np.float16:
                    result[vstart:self['vl']] = np.where( np.isposinf( result[vstart:self['vl']] ), 65504, result[vstart:self['vl']] )     
                                 
                libm.fesetround( 0 )               

            return result
        else:
            return 0


class Vfcvt_f_x_v(Inst):
    name = 'vfcvt.f.x.v'
    type_dict = { 16:np.float16, 32:np.float32, 64:np.float64 }

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfcvt_f_x_v.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self['vs2'][vstart:self['vl']].astype(Vfcvt_f_x_v.type_dict[self['ebits']]),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0          

