from ...isa.inst import *
import numpy as np

class Vfslide1up_vf(Inst):
    name = 'vfslide1up.vf'

    def golden(self):

        if 'rs1' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['rs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0

            if vstart == 0:
                if 'mask' not in self:
                    result[0] = self['rs1']
                else:
                    if self['mask'][0] & 0x1 == 1:
                        result[0] = self['rs1']
            

            result[max(vstart, 1):self['vl']] = self.masked( self['vs2'][max(vstart,1)-1:self['vl']-1], self['orig'][max(vstart, 1):self['vl']] if 'orig' in self else 0, max(vstart, 1) )
            
            return result
        else:
            return 0


class Vfslide1down_vf(Inst):
    name = 'vfslide1down.vf'

    def golden(self):

        if 'rs1' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( self['vl'], dtype = self['rs1'].dtype )

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0
            
            vd = np.concatenate( (self['vs2'][0:self['vl']], self['rs1']), axis=0 )
            result[vstart:self['vl']] = self.masked( vd[vstart+1:self['vl']+1], self['orig'][vstart:self['vl']] if 'orig' in self else 0, vstart )
            
            return result
        else:
            return 0


