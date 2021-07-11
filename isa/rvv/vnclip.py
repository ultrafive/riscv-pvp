from isa.inst import *
import math

class Vnclipu_wv(Inst):
    name = 'vnclipu.wv'
    def golden(self):
        UINT64_MAX = 18446744073709551615   #0xffffffffffffffff
        uint_max   = UINT64_MAX >> (64-self['sew'])
        sign_mask  = UINT64_MAX << (self['sew'])

        maskflag = 1 if 'mask' in self else 0 
        for ii in range(self['vl']):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                shift = self['vs1'][ii]&(2*self['sew']-1)
                temp  = self.rounding(self['vs2'][ii], self['vxrm'], shift)
                self['ori'][ii] = np.right_shift(temp, shift)
                if self['ori'][ii] & sign_mask:
                    self['ori'][ii] = uint_max
                    print('exit saturation')
        return self['ori']

class Vnclipu_wx(Inst):
    name = 'vnclipu.wx'
    def golden(self):
        UINT64_MAX = 18446744073709551615
        uint_max   = UINT64_MAX >> (64-self['sew'])
        sign_mask  = UINT64_MAX << (self['sew'])

        maskflag = 1 if 'mask' in self else 0 
        shift = self['rs1']&(2*self['sew']-1)
        for ii in range(self['vl']):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                temp  = self.rounding(self['vs2'][ii], self['vxrm'], shift)
                self['ori'][ii] = np.right_shift(temp, shift)
                if self['ori'][ii] & sign_mask:
                    self['ori'][ii] = uint_max
                    print('exit saturation')
        return self['ori']


class Vnclipu_wi(Inst):
    name = 'vnclipu.wi'
    def golden(self):
        UINT64_MAX = 18446744073709551615
        uint_max   = UINT64_MAX >> (64-self['sew'])
        sign_mask  = UINT64_MAX << (self['sew'])

        maskflag = 1 if 'mask' in self else 0 
        shift = self['uimm']&(2*self['sew']-1)
        for ii in range(self['vl']):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                temp  = self.rounding(self['vs2'][ii], self['vxrm'], shift)
                self['ori'][ii] = np.right_shift(temp, shift)
                if self['ori'][ii] & sign_mask:
                    self['ori'][ii] = uint_max
                    print('exit saturation')
        return self['ori']


class Vnclip_wv(Inst):
    name = 'vnclip.wv'
    def golden(self):
        INT64_MAX = 9223372036854775807    #0x7fffffffffffffff
        INT64_MIN = ((-INT64_MAX)-1)
        int_max   = INT64_MAX >> (64-self['sew'])
        int_min   = INT64_MIN >> (64-self['sew'])

        maskflag = 1 if 'mask' in self else 0 
        
        for ii in range(self['vl']):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):
                shift = self['vs1'][ii]&(2*self['sew']-1)
                temp  = self.rounding(self['vs2'][ii], self['vxrm'], shift)
                self['ori'][ii] = np.right_shift(temp, shift)
                if self['ori'][ii] > int_max:
                    self['ori'][ii] = int_max
                    print('exit saturation: upflow')
                if self['ori'][ii] < int_min:
                    self['ori'][ii] = int_min
                    print('exit saturation: downflow')
        return self['ori']


class Vnclip_wx(Inst):
    name = 'vnclip.wx'
    def golden(self):
        INT64_MAX = 9223372036854775807    
        INT64_MIN = ((-INT64_MAX)-1)
        int_max   = INT64_MAX >> (64-self['sew'])
        int_min   = INT64_MIN >> (64-self['sew'])

        maskflag = 1 if 'mask' in self else 0 
        shift = self['rs1']&(2*self['sew']-1)

        for ii in range(self['vl']):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):               
                temp  = self.rounding(self['vs2'][ii], self['vxrm'], shift)
                self['ori'][ii] = np.right_shift(temp, shift)
                if self['ori'][ii] > int_max:
                    self['ori'][ii] = int_max
                    print('exit saturation: upflow')
                if self['ori'][ii] < int_min:
                    self['ori'][ii] = int_min
                    print('exit saturation: downflow')
        return self['ori']

class Vnclip_wi(Inst):
    name = 'vnclip.wi'
    def golden(self):
        INT64_MAX = 9223372036854775807    
        INT64_MIN = ((-INT64_MAX)-1)
        int_max   = INT64_MAX >> (64-self['sew'])
        int_min   = INT64_MIN >> (64-self['sew'])

        maskflag = 1 if 'mask' in self else 0 
        shift = self['uimm']&(2*self['sew']-1)

        for ii in range(self['vl']):
            if (maskflag == 0) or (maskflag == 1 and np.bitwise_and(np.uint64(self['mask'][0]), np.uint64(2**ii)) ):               
                temp  = self.rounding(self['vs2'][ii], self['vxrm'], shift)
                self['ori'][ii] = np.right_shift(temp, shift)
                if self['ori'][ii] > int_max:
                    self['ori'][ii] = int_max
                    print('exit saturation: upflow')
                if self['ori'][ii] < int_min:
                    self['ori'][ii] = int_min
                    print('exit saturation: downflow')
        return self['ori']

