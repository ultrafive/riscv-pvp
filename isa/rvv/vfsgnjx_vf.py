from isa.inst import *
import numpy as np
import struct

class Vfsgnjx_vf(Inst):
    name = 'vfsgnjx.vf'

    def golden(self):
        
        vd = np.zeros( self['vs2'].size, dtype = self['vs2'].dtype )
        for i, v in enumerate(self['vs2']):
            vd[i] = np.where( struct.unpack( '<I', struct.pack( '<f', self['rs1'] ) )[0] >> 31 == 
            struct.unpack( '<I', struct.pack( '<f', self['vs2'][i] ) )[0] >> 31, abs( self['vs2'][i] ), -abs( self['vs2'][i] ) )

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd
