from isa.inst import *
import numpy as np
import math

class Vfwcvt_xu_f_v(Inst):
    name = 'vfwcvt.xu.f.v'
    type_dict = { 16:np.uint32, 32:np.uint64 }
    max_dict = { 16:4294967295, 32:18446744073709551615 }

    def convert( self, a ):
        b = np.where( a < 0, 0, a )
        target_dtype = Vfwcvt_xu_f_v.type_dict[self['ebits']]        

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

        b = np.where( np.isnan(a), Vfwcvt_xu_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfwcvt_xu_f_v.max_dict[self['ebits']], b )

        b = np.where( a > Vfwcvt_xu_f_v.max_dict[self['ebits']], Vfwcvt_xu_f_v.max_dict[self['ebits']], b )        

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfwcvt_xu_f_v.type_dict[self['ebits']] )

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

class Vfwcvt_x_f_v(Inst):
    name = 'vfwcvt.x.f.v'
    type_dict = { 16:np.int32, 32:np.int64 }
    max_dict = { 16:2147483647, 32:9223372036854775807 }
    min_dict = { 16:-2147483648, 32:-9223372036854775808 }

    def convert( self, a ):
        b = a
        target_dtype = Vfwcvt_x_f_v.type_dict[self['ebits']]        

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

        b = np.where( np.isnan(a), Vfwcvt_x_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfwcvt_x_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isneginf(a), Vfwcvt_x_f_v.min_dict[self['ebits']], b )

        b = np.where( a > Vfwcvt_x_f_v.max_dict[self['ebits']], Vfwcvt_x_f_v.max_dict[self['ebits']], b ) 
        b = np.where( a < Vfwcvt_x_f_v.min_dict[self['ebits']], Vfwcvt_x_f_v.min_dict[self['ebits']], b )       

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfwcvt_x_f_v.type_dict[self['ebits']] )

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

class Vfwcvt_rtz_xu_f_v(Inst):
    name = 'vfwcvt.rtz.xu.f.v'
    type_dict = { 16:np.uint32, 32:np.uint64 }
    max_dict = { 16:4294967295, 32:18446744073709551615 }

    def convert( self, a ):
        b = np.where( a < 0, 0, a )
        target_dtype = Vfwcvt_rtz_xu_f_v.type_dict[self['ebits']]        

        #rtz
        b = np.trunc( b )
        b = b.astype( target_dtype )


        b = np.where( np.isnan(a), Vfwcvt_rtz_xu_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfwcvt_rtz_xu_f_v.max_dict[self['ebits']], b )

        b = np.where( a > Vfwcvt_rtz_xu_f_v.max_dict[self['ebits']], Vfwcvt_rtz_xu_f_v.max_dict[self['ebits']], b )        

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfwcvt_rtz_xu_f_v.type_dict[self['ebits']] )

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

class Vfwcvt_rtz_x_f_v(Inst):
    name = 'vfwcvt.rtz.x.f.v'
    type_dict = { 16:np.int32, 32:np.int64 }
    max_dict = { 16:2147483647, 32:9223372036854775807 }
    min_dict = { 16:-2147483648, 32:-9223372036854775808 }

    def convert( self, a ):
        b = a
        target_dtype = Vfwcvt_rtz_x_f_v.type_dict[self['ebits']]        

        #rtz
        b = np.trunc( b )
        b = b.astype( target_dtype )


        b = np.where( np.isnan(a), Vfwcvt_rtz_x_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isposinf(a), Vfwcvt_rtz_x_f_v.max_dict[self['ebits']], b )

        b = np.where( np.isneginf(a), Vfwcvt_rtz_x_f_v.min_dict[self['ebits']], b )

        b = np.where( a > Vfwcvt_rtz_x_f_v.max_dict[self['ebits']], Vfwcvt_rtz_x_f_v.max_dict[self['ebits']], b ) 
        b = np.where( a < Vfwcvt_rtz_x_f_v.min_dict[self['ebits']], Vfwcvt_rtz_x_f_v.min_dict[self['ebits']], b )       

        return b

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfwcvt_rtz_x_f_v.type_dict[self['ebits']] )

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

class Vfwcvt_f_xu_v(Inst):
    name = 'vfwcvt.f.xu.v'
    type_dict = { 8:np.float16, 16:np.float32, 32:np.float64 }

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfwcvt_f_xu_v.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self['vs2'][vstart:self['vl']].astype(Vfwcvt_f_xu_v.type_dict[self['ebits']]),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0


class Vfwcvt_f_x_v(Inst):
    name = 'vfwcvt.f.x.v'
    type_dict = { 8:np.float16, 16:np.float32, 32:np.float64 }

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfwcvt_f_x_v.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self['vs2'][vstart:self['vl']].astype(Vfwcvt_f_x_v.type_dict[self['ebits']]),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0                 

class Vfwcvt_f_f_v(Inst):
    name = 'vfwcvt.f.f.v'
    type_dict = { 16:np.float32, 32:np.float64 }

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = Vfwcvt_f_f_v.type_dict[self['ebits']] )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0            

            result[ vstart: self['vl'] ] = self.masked( self['vs2'][vstart:self['vl']].astype(Vfwcvt_f_f_v.type_dict[self['ebits']]),
             self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )

            return result
        else:
            return 0 
