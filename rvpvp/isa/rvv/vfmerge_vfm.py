from ...isa.inst import *
import numpy as np

class Vfmerge_vfm(Inst):
    name = 'vfmerge.vfm'

    def golden(self):
        if 'vs2' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['vs2'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            result[vstart:self['vl']] = self.masked( self['rs1'].astype( self['vs2'].dtype ),
             self['vs2'][vstart:self['vl']], vstart )
            
            return result
        else:
            return 0 
