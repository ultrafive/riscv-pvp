from isa.inst import *
import numpy as np

class Vadc_vim(Inst):
    name = 'vadc.vim'
    # vadc.vim vd, vs2, imm, v0   
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart = self['vstart'] if 'vstart' in self else 0 
        mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']] 
        for ii in range(vstart, self['vl']): 
            result[ii] = self['vs2'][ii].astype(object) + self['imm'] + mask[ii]
        return result 


class Vmerge_vim(Inst):
    name = 'vmerge.vim'
    # vmerge.vim vd, vs2, imm, v0   
    def golden(self):     
        if self['vl']==0:
            return self['ori']
        result = self['ori'].copy()
        vstart = self['vstart'] if 'vstart' in self else 0 
        mask = np.unpackbits(self['mask'], bitorder='little')[0: self['vl']]
        for ii in range(vstart, self['vl']): 
            result[ii] = self['imm'] if mask[ii] else self['vs2'][ii]
        return result 

