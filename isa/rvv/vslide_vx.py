from isa.inst import *
import numpy as np


def getVLMAX(sew, lmul):
    vldefault = 1024
    lmulKey = {'1': 1, '2': 2, '4': 4, '8': 8, 'f2': 1/2, 'f4': 1/4, 'f8': 1/8}
    return int(lmulKey[str(lmul)] * vldefault / sew)

##return the value 0 when the index is greater than VLMAX in the source vector register group
def indexIsGreaterThanVLMAX(sew, lmul, vl, result):
    VLMAX = getVLMAX(sew, lmul)
    if vl >= VLMAX:
        for ii in range(VLMAX, vl, 1):
            result[ii] = 0x0


class Vslide1up_vx(Inst):
    name = 'vslide1up.vx'
    '''         i < vstart              unchanged 
            0 = i = vstart              vd[i] = x[rs1] if v0.mask[i] enabled
        max(vstart, 1) <= i < vl        vd[i] = vs2[i-1] if v0.mask[i] enabled  
            vl <= i < VLMAX             Follow tail policy
    '''
    def golden(self):
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0       
        if vstart == 0:
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**0)) ):
                self['ori'][0] = self['rs1']
      
        idx = max(vstart, 1)   
        if idx < self['vl']:
            for ii in range(idx, self['vl'], 1):
                if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii))):
                    self['ori'][ii] = self['vs2'][ii-1]   

        indexIsGreaterThanVLMAX(self['sew'], self['lmul'], self['vl'], self['ori'])
        return self['ori']


class Vslideup_vx(Inst):
    name = 'vslideup.vx'
    '''         0 < i < max(vstart, OFFSET)     Unchanged
          max(vstart, OFFSET) <= i < vl         vd[i] = vs2[i-OFFSET] if v0.mask[i] enabled  
                vl <= i < VLMAX                 Follow tail policy
    '''
    def golden(self):      
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0     
        idx = max(vstart, self['rs1']) 
        if idx < self['vl']:
            for ii in range(idx, self['vl'], 1):
                if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                    self['ori'][ii] = self['vs2'][ii-int(self['rs1'])]   

        indexIsGreaterThanVLMAX(self['sew'], self['lmul'], self['vl'] , self['ori'])
        return self['ori']


class Vslide1down_vx(Inst):
    name = 'vslide1down.vx'
    '''       i < vstart            unchanged 
        vstart <= i < vl-1          vd[i] = vs2[i+1] if v0.mask[i] enabled 
        vstart <= i = vl-1          vd[vl-1] = x[rs1] if v0.mask[i] enabled  
            vl <= i < VLMAX         Follow tail policy
    '''
    def golden(self):
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0     
        if vstart < self['vl']-1:
            for ii in range(vstart, self['vl']-1, 1):
                if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                    self['ori'][ii] = self['vs2'][ii+1] 

        VLMAX = getVLMAX(self['sew'], self['lmul'])
        vlValid = min(VLMAX, self['vl'])      
        if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**(vlValid-1))) ):      
            self['ori'][vlValid-1] = self['rs1'] 

        indexIsGreaterThanVLMAX(self['sew'], self['lmul'], self['vl'], self['ori'])
        return self['ori']


class Vslidedown_vx(Inst):
    name = 'vslidedown.vx'
    '''         0 < i < vstart    Unchanged
          vstart <= i < vl        vd[i] = src[i] if v0.mask[i] enabled 
              vl <= i < VLMAX     Follow tail policy
    '''
    def golden(self):
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0        
        if vstart < self['vl']:
            for ii in range(vstart, self['vl'], 1):
                if (ii+self['rs1']) >= self['vl'] :
                    if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                        self['ori'][ii] = 0x0
                else:
                    if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                        self['ori'][ii] = self['vs2'][ii+int(self['rs1'])] 

        indexIsGreaterThanVLMAX(self['sew'], self['lmul'], self['vl'], self['ori'])
        return self['ori']