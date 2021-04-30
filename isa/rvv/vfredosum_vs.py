from isa.inst import *
import numpy as np

class Vfredosum_vs(Inst):
    name = 'vfredosum.vs'

    def golden(self):
        vd = self['orig'].copy()
        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( 1 - (( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 ) )
            mask = np.array(mask).astype( bool )
            if mask.all() == True:
                vd[0] = self['vs1'][0]
            else:
                vd[0] = self['vs1'][0] + np.ma.array( self['vs2'], mask=mask ).sum()
        else:
            vd[0] = self['vs1'][0] + self['vs2'].sum()

        return vd
