from isa.inst import *
import numpy as np

class Vfmin_vf(Inst):
    name = 'vfmin.vf'

    def golden(self):
        vd = np.zeros( self['vs2'].size, dtype=self['vs2'].dtype )
        for no in range(0, self['vs2'].size):
            if np.isnan( self['rs1'].astype( self['vs2'].dtype ) ):
                vd[no] = self['vs2'][no]
            elif np.isnan( self['vs2'][no] ):
                vd[no] == self['rs1'].astype( self['vs2'].dtype )
            else:
                if self['rs1'].astype( self['vs2'].dtype ) < self['vs2'][no]:
                    vd[no] = self['rs1'].astype( self['vs2'].dtype )
                else:
                    vd[no] = self['vs2'][no]

        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd
