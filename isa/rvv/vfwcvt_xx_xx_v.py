from isa.inst import *
import numpy as np
import math

class Vfwcvt_xu_f_v(Inst):
    name = 'vfwcvt.xu.f.v'

    def golden(self):

        vd = np.where( self['vs2'] < 0, 0, self['vs2'] )

        if self['vs2'].dtype == np.float16:
            target_dtype = np.uint32
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.uint64

        if self['frm'] == 0:
            #rne
            vd = np.rint( vd )
            vd = vd.astype( target_dtype )
        elif self['frm'] == 1:
            #rtz
            vd = np.trunc( vd )
            vd = vd.astype( target_dtype )
        elif self['frm'] == 2:
            #rdn
            vd = np.floor( vd )
            vd = vd.astype( target_dtype )
        elif self['frm'] == 3:
            #rup
            vd = np.ceil( vd )
            vd = vd.astype( target_dtype )
        elif self['frm'] == 4:
            #rmm
            vd = np.where( vd - np.trunc( vd ) == 0.5, vd + 0.1, vd )
            vd = np.rint( vd )
            vd = vd.astype( target_dtype )

        if self['vs2'].dtype == np.float16:
            vd = np.where( self['vs2'] >= 4294967295, 4294967295, vd )
        elif self['vs2'].dtype == np.float32:
            vd = np.where( self['vs2'] >= 18446744073709551615, 18446744073709551615, vd )
        
        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vfwcvt_x_f_v(Inst):
    name = 'vfwcvt.x.f.v'

    def golden(self):

        if self['vs2'].dtype == np.float16:
            target_dtype = np.int32           
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.int64
        
        vd = self['vs2']
                    

        if self['frm'] == 0:
            #rne
            vd = np.rint( vd )
            vd = vd.astype( target_dtype )
        elif self['frm'] == 1:
            #rtz
            vd = np.trunc( vd )
            vd = vd.astype( target_dtype )
        elif self['frm'] == 2:
            #rdn
            vd = np.floor( vd )
            vd = vd.astype( target_dtype )
        elif self['frm'] == 3:
            #rup
            vd = np.ceil( vd )
            vd = vd.astype( target_dtype )
        elif self['frm'] == 4:
            #rmm
            vd = np.where( vd - np.trunc( vd ) == 0.5, vd + 0.3, vd )
            vd = np.where( vd - np.trunc( vd ) == -0.5, vd -0.5, vd )
            vd = np.rint( vd )
            vd = vd.astype( target_dtype )

        if self['vs2'].dtype == np.float16:
            vd = np.where( self['vs2'] >= 2147483647, 2147483647, vd )   
            vd = np.where( self['vs2'] <= -2147483648, -2147483648, vd )            
        elif self['vs2'].dtype == np.float32:
            vd = np.where( self['vs2'] >= 9223372036854775807, 9223372036854775807, vd )   
            vd = np.where( self['vs2'] <= -9223372036854775808, -9223372036854775808, vd )             

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vfwcvt_rtz_xu_f_v(Inst):
    name = 'vfwcvt.rtz.xu.f.v'

    def golden(self):

        vd = np.where( self['vs2'] < 0, 0, self['vs2'] )

        if self['vs2'].dtype == np.float16:
            target_dtype = np.uint32
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.uint64

        vd = np.trunc( vd )
        vd = vd.astype( target_dtype )

        if self['vs2'].dtype == np.float16:
            vd = np.where( self['vs2'] >= 4294967295, 4294967295, vd )
        elif self['vs2'].dtype == np.float32:
            vd = np.where( self['vs2'] >= 18446744073709551615, 18446744073709551615, vd )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vfwcvt_rtz_x_f_v(Inst):
    name = 'vfwcvt.rtz.x.f.v'

    def golden(self):

        if self['vs2'].dtype == np.float16:
            target_dtype = np.int32         
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.int64          

        vd = np.trunc( self['vs2'] )
        vd = vd.astype( target_dtype )

        if self['vs2'].dtype == np.float16:
            vd = np.where( self['vs2'] >= 2147483647, 2147483647, vd )   
            vd = np.where( self['vs2'] <= -2147483648, -2147483648, vd )           
        elif self['vs2'].dtype == np.float32:
            vd = np.where( self['vs2'] >= 9223372036854775807, 9223372036854775807, vd )   
            vd = np.where( self['vs2'] <= -9223372036854775808, -9223372036854775808, vd ) 

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vfwcvt_f_xu_v(Inst):
    name = 'vfwcvt.f.xu.v'

    def golden(self):

        if self['vs2'].dtype == np.uint16:
            target_dtype = np.float32
        elif self['vs2'].dtype == np.uint32:
            target_dtype = np.float64

        vd = self['vs2'].astype( target_dtype )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vfwcvt_f_x_v(Inst):
    name = 'vfwcvt.f.x.v'

    def golden(self):

        if self['vs2'].dtype == np.int16:
            target_dtype = np.float32
        elif self['vs2'].dtype == np.int32:
            target_dtype = np.float64

        vd = self['vs2'].astype( target_dtype )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )        

class Vfwcvt_f_f_v(Inst):
    name = 'vfwcvt.f.f.v'

    def golden(self):

        if self['vs2'].dtype == np.float16:
            target_dtype = np.float32
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.float64

        vd = self['vs2'].astype( target_dtype )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )
