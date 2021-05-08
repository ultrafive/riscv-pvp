from isa.inst import *
import numpy as np
import math

class Vfcvt_xu_f_v(Inst):
    name = 'vfcvt.xu.f.v'

    def golden(self):

        vd = np.where( self['vs2'] < 0, 0, self['vs2'] )

        if self['vs2'].dtype == np.float16:
            target_dtype = np.uint16
            vd = np.where( vd > 65535, 65535, vd )
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.uint32
            vd = np.where( vd > 4294967295, 4294967295, vd )
        elif self['vs2'].dtype == np.float64:
            target_dtype = np.uint64
            vd = np.where( vd > 18446744073709551615, 18446744073709551615, vd )

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

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vfcvt_x_f_v(Inst):
    name = 'vfcvt.x.f.v'

    def golden(self):

        if self['vs2'].dtype == np.float16:
            target_dtype = np.int16
            vd = np.where( self['vs2'] > 32767, 32767, self['vs2'] )   
            vd = np.where( vd < -32768, -32768, vd )            
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.int32
            vd = np.where( self['vs2'] > 2147483647, 2147483647, self['vs2'] )   
            vd = np.where( vd < -2147483648, -2147483648, vd )           
        elif self['vs2'].dtype == np.float64:
            target_dtype = np.int64
            vd = np.where( self['vs2'] > 9223372036854775807, 9223372036854775807, self['vs2'] )   
            vd = np.where( vd < -9223372036854775808, -9223372036854775808, vd )            

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

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vfcvt_rtz_xu_f_v(Inst):
    name = 'vfcvt.rtz.xu.f.v'

    def golden(self):

        vd = np.where( self['vs2'] < 0, 0, self['vs2'] )

        if self['vs2'].dtype == np.float16:
            target_dtype = np.uint16
            vd = np.where( vd > 65535, 65535, vd )
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.uint32
            vd = np.where( vd > 4294967295, 4294967295, vd )
        elif self['vs2'].dtype == np.float64:
            target_dtype = np.uint64
            vd = np.where( vd > 18446744073709551615, 18446744073709551615, vd )

        vd = np.trunc( vd )
        vd = vd.astype( target_dtype )
        

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )  

class Vfcvt_rtz_x_f_v(Inst):
    name = 'vfcvt.rtz.x.f.v'

    def golden(self):

        if self['vs2'].dtype == np.float16:
            target_dtype = np.int16
            vd = np.where( self['vs2'] > 32767, 32767, self['vs2'] )   
            vd = np.where( vd < -32768, -32768, vd )            
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.int32
            vd = np.where( self['vs2'] > 2147483647, 2147483647, self['vs2'] )   
            vd = np.where( vd < -2147483648, -2147483648, vd )           
        elif self['vs2'].dtype == np.float64:
            target_dtype = np.int64
            vd = np.where( self['vs2'] > 9223372036854775807, 9223372036854775807, self['vs2'] )   
            vd = np.where( vd < -9223372036854775808, -9223372036854775808, vd ) 

        vd = np.trunc( vd )
        vd = vd.astype( target_dtype )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )


class Vfcvt_f_xu_v(Inst):
    name = 'vfcvt.f.xu.v'

    def golden(self):

        if self['vs2'].dtype == np.uint16:
            target_dtype = np.float16
        elif self['vs2'].dtype == np.uint32:
            target_dtype = np.float32
        elif self['vs2'].dtype == np.uint64:
            target_dtype = np.float64

        vd = self['vs2'].astype( target_dtype )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )

class Vfcvt_f_x_v(Inst):
    name = 'vfcvt.f.x.v'

    def golden(self):

        if self['vs2'].dtype == np.int16:
            target_dtype = np.float16
        elif self['vs2'].dtype == np.int32:
            target_dtype = np.float32
        elif self['vs2'].dtype == np.int64:
            target_dtype = np.float64

        vd = self['vs2'].astype( target_dtype )

        return self.masked( vd, self['orig'] if 'orig' in self else 0 )           

