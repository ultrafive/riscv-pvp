from isa.inst import *
import numpy as np
import math

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

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd