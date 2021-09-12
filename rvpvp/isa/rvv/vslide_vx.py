from ...isa.inst import *
import numpy as np

class Vslide1up_vx(Inst):
    name = 'vslide1up.vx'
    # vslide1up.vx vd, vs2, rs1, vm # vd[0]=x[rs1], vd[i+1] = vs2[i] 
    '''         i < vstart              unchanged 
            0 = i = vstart              vd[i] = x[rs1] if v0.mask[i] enabled
        max(vstart, 1) <= i < vl        vd[i] = vs2[i-1] if v0.mask[i] enabled  
            vl <= i < VLMAX             Follow tail policy
    '''
    def golden(self):
        if 0 == self['vl']:
            return self['ori']
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0 
        result = self['ori'].copy()      
        if vstart == 0:
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[0] ):
                result[0] = self['rs1']
      
        idx = max(vstart, 1)   
        if idx < self['vl']:
            for ii in range(idx, self['vl'], 1):
                if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                    result[ii] = self['vs2'][ii-1]   

        return result


class Vslideup_vx(Inst):
    name = 'vslideup.vx'
    # vslideup.vx vd, vs2, rs1, vm # vd[i+rs1] = vs2[i] 
    '''         0 < i < max(vstart, OFFSET)     Unchanged
          max(vstart, OFFSET) <= i < vl         vd[i] = vs2[i-OFFSET] if v0.mask[i] enabled  
                vl <= i < VLMAX                 Follow tail policy
    '''
    def golden(self):  
        result = self['ori'].copy()
        if 0 == self['vl']:
            return result   
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0     
        idx = max(vstart, self['rs1']) 
        if idx < self['vl']:
            for ii in range(idx, self['vl'], 1):
                if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                    result[ii] = self['vs2'][ii-int(self['rs1'])]   

        return result


class Vslide1down_vx(Inst):
    name = 'vslide1down.vx'
    # vslide1up.vx vd, vs2, rs1, vm # vd[0]=x[rs1], vd[i+1] = vs2[i] 
    '''       i < vstart            unchanged 
        vstart <= i < vl-1          vd[i] = vs2[i+1] if v0.mask[i] enabled 
        vstart <= i = vl-1          vd[vl-1] = x[rs1] if v0.mask[i] enabled  
            vl <= i < VLMAX         Follow tail policy
    '''
    def golden(self):
        result = self['ori'].copy()
        if 0 == self['vl']:
            return result
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0     
        if vstart < self['vl']-1:
            for ii in range(vstart, self['vl']-1, 1):
                if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                    result[ii] = self['vs2'][ii+1] 

        vlValid = min(self.VLMAX(self['sew'],self['lmul']), self['vl'])   
        if vstart <= vlValid-1:
            if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[vlValid-1] ):       
                result[vlValid-1] = self['rs1'] 

        return result


class Vslidedown_vx(Inst):
    name = 'vslidedown.vx'
    # vslidedown.vx vd, vs2, rs1, vm # vd[i] = vs2[i+rs1]
    '''         0 < i < vstart    Unchanged
          vstart <= i < vl        vd[i] = src[i] if v0.mask[i] enabled 
              vl <= i < VLMAX     Follow tail policy
    '''
    def golden(self):
        result = self['ori'].copy()
        if 0 == self['vl']:
            return result
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0  

        if vstart < self['vl']:
            for ii in range(vstart, self['vl'], 1):
                if (maskflag == 0) or (maskflag == 1 and np.unpackbits(self['mask'], bitorder='little')[ii] ):
                    if (ii+self['rs1']) >= self['vl'] :                    
                        if 'tail' in self:
                            if (ii+self['rs1']) < self.VLMAX(self['sew'],self['lmul']) :
                                result[ii] = self['vs2'][ii+int(self['rs1'])] 
                            else:
                                result[ii] = 0x0
                        else:
                            result[ii] = 0x0
                    else:
                        result[ii] = self['vs2'][ii+int(self['rs1'])] 

        return result
        