from isa.inst import *
import numpy as np

class Vmfeq_vv(Inst):
    name = 'vmfeq.vv'

    def golden(self):
        if 'v0' in self:
            mask = []
            orig = []
            orig_data = self["orig"].copy()
            orig_data.dtype = np.uint8
            for no in range(0, self['vs1'].size):
                mask.append( ( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
                orig.append( ( orig_data[np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 )
            mask = np.array(mask)
            orig = np.array(orig).astype(np.bool_)
            return np.where( mask == 1, ( self['vs1'] == self['vs2'] ).astype( np.bool_ ), orig)
        else:
            return ( self['vs1'] == self['vs2'] ).astype( np.bool_ )
