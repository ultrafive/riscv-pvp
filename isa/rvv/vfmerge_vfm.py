from isa.inst import *
import numpy as np

class Vfmerge_vfm(Inst):
    name = 'vfmerge.vfm'

    def golden(self):

        mask = []
        for no in range(0, self['vs2'].size):
            mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
        mask = np.array(mask)

        return np.where( mask == 1, self['rs1'].astype( self['vs2'].dtype ), self['vs2'] )
