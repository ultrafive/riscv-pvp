from isa.inst import *
import numpy as np
import math

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

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd