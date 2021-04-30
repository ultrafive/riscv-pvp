from isa.inst import *
import numpy as np
import struct

class Vfsgnj_vv(Inst):
    name = 'vfsgnj.vv'

    def golden(self):
        if self['vs1'].dtype == np.float16:
            str_int = '<H'
            str_float = '<e'
            signal_bit = 15
        elif self['vs1'].dtype == np.float32:
            str_int = '<I'
            str_float = '<f'
            signal_bit = 31            

        elif self['vs1'].dtype == np.float64:
            str_int = '<Q'
            str_float = '<d'
            signal_bit = 63
        
        vd = np.zeros( self['vs2'].size, dtype = self['vs2'].dtype )
        for i, v in enumerate(self['vs1']):
            vd[i] = np.where( struct.unpack( str_int, struct.pack( str_float, v ) )[0] >> signal_bit, -abs( self['vs2'][i] ), abs( self['vs2'][i] ) )

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs1'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd
