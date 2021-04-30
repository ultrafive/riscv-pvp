from isa.inst import *
import numpy as np

class Vfredmax_vs(Inst):
    name = 'vfredmax.vs'

    def golden(self):
        vd = self['orig'].copy()
        vs1= self['vs1'].copy()
        if np.isnan( vs1[0] ):
            vs1[0] = np.NINF
        vs2 = self['vs2'].copy()
        for no in range(0, vs2.size):
            if np.isnan( vs2[no] ):
                vs2[no] = np.NINF        
        if 'v0' in self:
            mask = []
            for no in range(0, self['vs2'].size):
                mask.append( 1 - (( self['v0'][np.floor(no/8).astype(np.int8)] >> (no % 8) ) & 1 ) )
                
            mask = np.array(mask).astype( bool )
            if mask.all() == True:
                vd[0] = vs1[0]
            else:            
                vd[0] = np.max( [ vs1[0], np.ma.array( vs2, mask=mask ).max() ] )
        else:
            vd[0] = np.max( [ vs1[0], vs2.max() ] )

        return vd
