from isa.inst import *
import math

class Vssrl_vv(Inst):
    name = 'vssrl.vv'
    def golden(self):
        result = self['ori'].tolist()
        maskflag = 1 if 'mask' in self else 0       
        for ii in range(len(result)):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                shift = self['vs1'][ii]&(self['sew']-1)
                temp = self.rounding(self['vs2'][ii], self['vxrm'], shift)
                result[ii] = np.right_shift(temp, shift )
        return np.array(result, dtype=self['ori'].dtype)

class Vssra_vv(Vssrl_vv):
    name = 'vssra.vv'


class Vssrl_vx(Inst):
    name = 'vssrl.vx'
    def golden(self):
        result = self['ori'].tolist()
        maskflag = 1 if 'mask' in self else 0 
        shift = self['rs1']&(self['sew']-1)
        for ii in range(len(result)):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                temp = self.rounding(self['vs2'][ii], self['vxrm'], shift)
                result[ii] = np.right_shift(temp, shift)
        return np.array(result, dtype=self['ori'].dtype)

class Vssra_vx(Vssrl_vx):
    name = 'vssra.vx'


class Vssrl_vi(Inst):
    name = 'vssrl.vi'
    def golden(self):
        result = self['ori'].tolist()
        maskflag = 1 if 'mask' in self else 0 
        shift = self['uimm']&(self['sew']-1)
        for ii in range(len(result)):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                temp = self.rounding(self['vs2'][ii], self['vxrm'], shift)
                result[ii] = np.right_shift(temp, shift)
        return np.array(result, dtype=self['ori'].dtype)

class Vssra_vi(Vssrl_vi):
    name = 'vssra.vi'
