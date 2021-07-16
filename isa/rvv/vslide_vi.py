from isa.inst import *
import numpy as np

def getVLMAX(sew, lmul):
    vlendefault = 1024
    lmulKey = {'1': 1, '2': 2, '4': 4, '8': 8, 'f2': 1/2, 'f4': 1/4, 'f8': 1/8}
    return int(lmulKey[str(lmul)] * vlendefault / sew)

##return the value 0 when the index is greater than VLMAX in the source vector register group
def indexIsGreaterThanVLMAX(sew, lmul, vl, result):
    VLMAX = getVLMAX(sew, lmul)
    if vl >= VLMAX:
        for ii in range(VLMAX, vl, 1):
            result[ii] = 0x0


class Vslideup_vi(Inst):
    name = 'vslideup.vi'
    def golden(self):      
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0       
        idx = max(vstart, self['uimm']) 
        if idx < self['vl']:
            for ii in range(idx, self['vl'], 1):
                if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                    self['ori'][ii] = self['vs2'][ii-int(self['uimm'])]   

        indexIsGreaterThanVLMAX(self['sew'], self['lmul'], self['vl'], self['ori'])
        return self['ori']


class Vslidedown_vi(Inst): 
    name = 'vslidedown.vi'
    def golden(self):
        vstart = self['vstart'] if 'vstart' in self else 0 
        maskflag = 1 if 'mask' in self else 0      
        if vstart < self['vl']:
            for ii in range(vstart, self['vl'], 1):
                if (ii+self['uimm']) >= self['vl'] :
                    if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                        self['ori'][ii] = 0x0
                else:
                    if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                        self['ori'][ii] = self['vs2'][ii+int(self['uimm'])] 

        indexIsGreaterThanVLMAX(self['sew'], self['lmul'], self['vl'], self['ori'])
        return self['ori']