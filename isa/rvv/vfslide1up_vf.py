from isa.inst import *
import numpy as np

class Vfslide1up_vf(Inst):
    name = 'vfslide1up.vf'

    def golden(self):

        vd = self['vs2'].tolist()
        vd.insert( 0, self['rs1'].astype( self['vs2'].dtype ) )
        vd = np.array(vd[:-1], dtype=self['vs2'].dtype )


        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            return np.where( mask == 1, vd, self['orig'])
        else:
            return vd