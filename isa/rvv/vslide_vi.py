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


class Vslideup_vi(Inst):
    name = 'vslideup.vi'
    def golden(self):      
        result = self['ori'].tolist()
        vs2    = self['vs2'].tolist()
        vstart = self['vstart'] if 'vstart' in self else 0 
        vl   = self['vl']   if 'vl'   in self else 0 
        maskflag = 1 if 'mask' in self else 0
        
        idx = max(vstart, self['uimm']) 
        if idx < len(vs2):
            for ii in range(idx, len(vs2), 1):
                if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                    result[ii] = vs2[ii-self['uimm']]   

        indexIsGreaterThanVLMAX(self['sew'], len(vs2), result)
        return np.array(result, dtype=self['vs2'].dtype )


class Vslidedown_vi(Inst): 
    name = 'vslidedown.vi'
    def golden(self):
        result = self['ori'].tolist()
        vs2    = self['vs2'].tolist()
        vstart = self['vstart'] if 'vstart' in self else 0 
        vl   = self['vl']   if 'vl'   in self else 0 
        maskflag = 1 if 'mask' in self else 0
          
        if vstart < vl:
            for ii in range(vstart, vl, 1):
                if (ii+self['uimm']) >= vl :
                    if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                        result[ii] = 0x0
                else:
                    if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                        result[ii] = vs2[ii+self['uimm']] 

        indexIsGreaterThanVLMAX(self['sew'], len(vs2), result)
        return np.array(result, dtype=self['vs2'].dtype )