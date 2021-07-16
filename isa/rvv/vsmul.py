from isa.inst import *
import numpy as np


def mulCvtDataType(sew, rs1, rs2):
    if    8 == sew:
        return rs1 * rs2.astype(np.int16)
    elif 16 == sew:
        return rs1 * rs2.astype(np.int32)
    elif 32 == sew:
        return rs1 * rs2.astype(np.int64)
    elif 64 == sew:# not support int64
        return rs1 * rs2.astype(np.longlong)
    else:   
        pass    



class Vsmul_vv(Inst):
    name = 'vsmul.vv'
    # vsmul.vv vd, vs2, vs1, vm 
    # vd[i] = clip(roundoff_signed(vs2[i]*vs1[i], SEW-1))
    def golden(self):
        INT64_MAX = 9223372036854775807    #0x7fffffffffffffff
        INT64_MIN = ((-INT64_MAX)-1)
        int_max   = INT64_MAX >> (64-self['sew'])
        int_min   = INT64_MIN >> (64-self['sew'])

        maskflag = 1 if 'mask' in self else 0 
        shift    = self['sew']-1
        

        for ii in range(self['vl']):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):                  
                mulValue = mulCvtDataType(self['sew'], self['vs1'][ii], self['vs2'][ii] )     
                temp  = self.rounding_xrm(mulValue, self['vxrm'], shift)
                self['ori'][ii] = np.right_shift(temp, shift) 
                if (self['vs1'][ii] == self['vs2'][ii]) and (self['vs1'][ii] == int_min):
                    self['ori'][ii] = int_max
                    print('exit saturation')
        return self['ori']


class Vsmul_vx(Inst):
    name = 'vsmul.vx'
    # vsmul.vx vd, vs2, rs1, vm 
    # vd[i] = clip(roundoff_signed(vs2[i]*x[rs1], SEW-1))
    def golden(self):
        INT64_MAX = 9223372036854775807    
        INT64_MIN = ((-INT64_MAX)-1)
        int_max   = INT64_MAX >> (64-self['sew'])
        int_min   = INT64_MIN >> (64-self['sew'])

        maskflag = 1 if 'mask' in self else 0 
        shift    = self['sew']-1

        for ii in range(self['vl']):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):   
                mulValue = mulCvtDataType(self['sew'], self['rs1'], self['vs2'][ii] )         
                temp  = self.rounding_xrm(mulValue, self['vxrm'], shift)
                self['ori'][ii] = np.right_shift(temp, shift) 
                if (self['rs1'] == self['vs2'][ii]) and (self['rs1'] == int_min) :
                    self['ori'][ii] = int_max
                    print('exit saturation')
        return self['ori']
