from ...isa.inst import *
import numpy as np

class Vfmv_v_f(Inst):
    name = 'vfmv.v.f'

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


            result[vstart:self['vl']] = self['rs1']
            
            return result
        else:
            return 0 

class Vfmv_s_f(Inst):
    name = 'vfmv.s.f'

    def golden(self):
        if 'rs1' in self:

            if 'orig' in self:
                result = self['orig'].copy()
            else:
                result = np.zeros( 1, dtype = self['rs1'].dtype )
            
            if 'vl' in self:
                vl = self['vl']
            else:
                vl = 0

            if 'vstart' in self:
                if self['vstart'] >= self['vl']:
                    return result
                vstart = self['vstart']
            else:
                vstart = 0


            if vl != 0:
                result[0] = self['rs1']
            
            return result
        else:
            return 0 

class Vfmv_f_s(Inst):
    name = 'vfmv.f.s'

    def golden(self):
        if 'vs2' in self:
            return np.array(self['vs2'][0])
        else:
            return 0
