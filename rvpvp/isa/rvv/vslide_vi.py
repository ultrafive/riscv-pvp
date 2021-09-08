from ...isa.inst import *
import numpy as np

class Vslideup_vi(Inst):
    name = 'vslideup.vi'
    # vslideup.vi vd, vs2, uimm, vm # vd[i+uimm] = vs2[i]
    def golden(self):  
        if 0 == self['vl']:
            return self['ori']
        result = self['ori'].copy()  
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0       
        idx = max(vstart, self['uimm']) 
        if idx < self['vl']:
            for ii in range(idx, self['vl']):
                if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                    result[ii] = self['vs2'][ii-int(self['uimm'])]   
        return result


class Vslidedown_vi(Inst): 
    name = 'vslidedown.vi'
    # vslidedown.vi vd, vs2, uimm, vm # vd[i] = vs2[i+uimm]
    def golden(self):       
        if 0 == self['vl']:
            return self['ori']
        result = self['ori'].copy()
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0      
        if vstart < self['vl']:
            for ii in range(vstart, self['vl'], 1):
                if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                    if (ii+self['uimm']) >= self['vl'] :                    
                        if 'tail' in self:
                            if (ii+self['uimm']) < self.get_VLMAX(self['sew'],self['lmul']):
                                result[ii] = self['vs2'][ii+int(self['uimm'])] 
                            else:
                                result[ii] = 0x0
                        else:
                            result[ii] = 0x0
                    else:
                        result[ii] = self['vs2'][ii+int(self['uimm'])] 
        return result
