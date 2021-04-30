from isa.inst import *
import numpy as np
import math

class Vfncvt_xu_f_w(Inst):
    name = 'vfncvt.xu.f.w'

    def golden(self):

        vd = np.where( self['vs2'] < 0, 0, self['vs2'] )

        if self['vs2'].dtype == np.float16:
            target_dtype = np.uint8
            vd = np.where( vd > 255, 255, vd )
        elif self['vs2'].dtype == np.float32:
            target_dtype = np.uint16
            vd = np.where( vd > 65535, 65535, vd )
        elif self['vs2'].dtype == np.float64:
            target_dtype = np.uint32
            vd = np.where( vd > 4294967295, 4294967295, vd )

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

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd