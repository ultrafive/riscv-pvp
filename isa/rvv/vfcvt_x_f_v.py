from isa.inst import *
import numpy as np
import math

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

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd