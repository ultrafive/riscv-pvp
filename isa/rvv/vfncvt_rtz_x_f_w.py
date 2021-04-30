from isa.inst import *
import numpy as np
import math

class Vfncvt_rtz_x_f_w(Inst):
    name = 'vfncvt.rtz.x.f.w'

    def golden(self):

        if self['vs2'].dtype == np.float16:
            target_dtype = np.int8
            vd = np.where( self['vs2'] > 127, 127, self['vs2'] )   
            vd = np.where( vd < -128, -128, vd )            
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.int16
            vd = np.where( self['vs2'] > 32767, 32767, self['vs2'] )   
            vd = np.where( vd < -32768, -32768, vd )          
        elif self['vs2'].dtype == np.float64:
            target_dtype = np.int32
            vd = np.where( self['vs2'] > 2147483647, 2147483647, self['vs2'] )   
            vd = np.where( vd < -2147483648, -2147483648, vd ) 

        vd = np.trunc( vd )
        vd = vd.astype( target_dtype )

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd