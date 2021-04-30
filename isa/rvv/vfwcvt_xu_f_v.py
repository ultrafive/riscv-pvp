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
        

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd