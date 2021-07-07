from isa.inst import *
import numpy as np

##return the value 0 when the index is greater than VLMAX in the source vector register group
def indexIsGreaterThanVLMAX(ebits, vs2len, result):
    vlendefault = 1024
    VLMAX = (vlendefault//ebits)
    print(str(VLMAX)+' VLMAX '+str(type(VLMAX)))
    if vs2len >= VLMAX:
        for ii in range(VLMAX, vs2len, 1):
            result[ii] = 0x0


class Vslide1up_vx(Inst):
    name = 'vslide1up.vx'
    '''         i < vstart              unchanged 
            0 = i = vstart              vd[i] = x[rs1] if v0.mask[i] enabled
        max(vstart, 1) <= i < vl        vd[i] = vs2[i-1] if v0.mask[i] enabled  
            vl <= i < VLMAX             Follow tail policy
    '''
    def golden(self):
        result = self['ori'].tolist()
        vs2    = self['vs2'].tolist()
        vstart = self['vstart'] if 'vstart' in self else 0 
        vl   = self['vl']   if 'vl'   in self else 0 
        maskflag = 1 if 'mask' in self else 0       
        if vstart == 0:
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**0)) ):
                result[0] = self['rs1']
      
        idx = max(vstart, 1)   
        if idx < vl:
            print(' polar '+ str(idx)+ '  '+str(vl)+ '  '+str(len(vs2)))
            for ii in range(idx, vl, 1):
                if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                    result[ii] = vs2[ii-1]   

        indexIsGreaterThanVLMAX(self['sew'], len(vs2), result)
        return np.array(result, dtype=self['vs2'].dtype )


class Vslideup_vx(Inst):
    name = 'vslideup.vx'
    '''         0 < i < max(vstart, OFFSET)     Unchanged
          max(vstart, OFFSET) <= i < vl         vd[i] = vs2[i-OFFSET] if v0.mask[i] enabled  
                vl <= i < VLMAX                 Follow tail policy
    '''
    def golden(self):      
        result = self['ori'].tolist()
        vs2    = self['vs2'].tolist()
        vstart = self['vstart'] if 'vstart' in self else 0 
        vl   = self['vl']   if 'vl'   in self else 0 
        maskflag = 1 if 'mask' in self else 0
        
        idx = max(vstart, self['rs1']) 
        if idx < len(vs2):
            for ii in range(idx, len(vs2), 1):
                if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                    result[ii] = vs2[ii-self['rs1']]   

        indexIsGreaterThanVLMAX(self['sew'], len(vs2), result)
        return np.array(result, dtype=self['vs2'].dtype )


class Vslide1down_vx(Inst):
    name = 'vslide1down.vx'
    '''       i < vstart            unchanged 
        vstart <= i < vl-1          vd[i] = vs2[i+1] if v0.mask[i] enabled 
        vstart <= i = vl-1          vd[vl-1] = x[rs1] if v0.mask[i] enabled  
            vl <= i < VLMAX         Follow tail policy
    '''
    def golden(self):
        result = self['ori'].tolist()
        vs2    = self['vs2'].tolist()
        vstart = self['vstart'] if 'vstart' in self else 0 
        vl   = self['vl']   if 'vl'   in self else 0 
        maskflag = 1 if 'mask' in self else 0
       
        if vstart < vl-1:
            for ii in range(vstart, vl-1, 1):
                if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                    result[ii] = vs2[ii+1] 

        vlendefault = 1024
        VLMAX = (vlendefault//self['sew'])
        vlValid = min(VLMAX, vl)      
        if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**(vlValid-1))) ):      
            result[vlValid-1] = self['rs1'] 

        indexIsGreaterThanVLMAX(self['sew'], len(vs2), result)
        return np.array(result, dtype=self['vs2'].dtype )


class Vslidedown_vx(Inst):
    name = 'vslidedown.vx'
    '''         0 < i < vstart    Unchanged
          vstart <= i < vl        vd[i] = src[i] if v0.mask[i] enabled 
              vl <= i < VLMAX     Follow tail policy
    '''
    def golden(self):
        result = self['ori'].tolist()
        vs2    = self['vs2'].tolist()
        vstart = self['vstart'] if 'vstart' in self else 0 
        vl   = self['vl']   if 'vl'   in self else 0 
        maskflag = 1 if 'mask' in self else 0
          
        if vstart < vl:
            for ii in range(vstart, vl, 1):
                if (ii+self['rs1']) >= vl :
                    if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                        result[ii] = 0x0
                else:
                    if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                        result[ii] = vs2[ii+self['rs1']] 

        indexIsGreaterThanVLMAX(self['sew'], len(vs2), result)
        return np.array(result, dtype=self['vs2'].dtype )