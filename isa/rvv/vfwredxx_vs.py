from isa.inst import *
import numpy as np

class Vfwredsum_vs(Inst):
    name = 'vfwredsum.vs'

    def golden(self):
        vd = self['orig'].copy()
        vs2 = self['vs2'].copy()
        vs2 = vs2.astype( vd.dtype )
        if 'mask' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( 1 - (( self['mask'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 ) )
            mask = np.array(mask).astype( bool )
            if mask.all() == True:
                vd[0] = self['vs1'][0]
            else:
                vd[0] = self['vs1'][0] + np.ma.array( vs2, mask=mask ).sum()
        else:
            vd[0] = self['vs1'][0] + vs2.sum()

        return vd

class Vfwredosum_vs(Vfwredsum_vs):
    name = 'vfwredosum.vs'       
