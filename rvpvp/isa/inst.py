
import sys
import numpy as np

factor_lmul = {
    1: 1, 2: 2, 4: 4, 8: 8,
    '1': 1, '2': 2, '4': 4, '8': 8,
    'f2': 1/2, 'f4': 1/4, 'f8': 1/8
}

class Inst(dict):
    name = 'unknown'

    def golden(self):
        raise NotImplementedError()

    def masked(self, value, old = 0, vstart = 0):
        if 'mask' not in self:
            return value
        else:
            mask = np.unpackbits(self['mask'], bitorder='little')[vstart: self['vl']]
            return np.where( mask == 1, value, old)


    def as_mask(self, value):
        return np.packbits(np.unpackbits(value, bitorder='little')[0: self['vl']], bitorder='little')
        
    
    def bits_copy(self, src, dst, start):
        src_bits = np.unpackbits(src, bitorder='little')
        dst_bits = np.unpackbits(dst, bitorder='little')
        dst_bits[start: self['vl']] = src_bits[start: self['vl']]
        return np.packbits(dst_bits, bitorder='little')


    def where(self):
        if 'mask' not in self:
            return True
        else:
            return np.unpackbits(self['mask'], bitorder='little')[0: self['vl']] == 1
    
    def rounding(self, value):
        if self['mode'] == 0:
            res = value + 1
        elif self['mode'] == 1:
            res = np.where(value%4==3, value+1, value)
        elif self['mode'] == 2:
            res = value
        elif self['mode'] == 3:
            res = np.where(value%4==1, value+2, value)

        return res


    def rounding_xrm(self, result, xrm, shift):
        # Suppose the pre-rounding result is v, and d bits of that result areto be rounded off. 
        # Then the rounded result is (v >> d) + r, where r depends on the rounding mode 
        # (result >> shift) + r

        if shift == 0:
            return result

        lsb  = 2**shift     # 1<<shift
        half = lsb//2       # lsb>>1        
        
        if xrm == 0:    #RNU:
            result += half      #RuntimeWarning: overflow encountered in long_scalars
        elif xrm == 1:  #RNE:
            #if (result & half) and ((result & (half-1)) or (result & lsb)) :
            if (result//half%2 == 1) and (result%half != 0 or result//lsb%2 == 1):
                result += lsb
        elif xrm == 2:  #RDN:
            pass
        elif xrm == 3:  #ROD:
            if result%lsb:                #result & (lsb - 1):                
                if result//lsb%2 == 0:    #result |= lsb          #casting rule 'safe'
                    result += lsb                
        else:
            print("error vrm para!")

        return result//(2**shift)


    def VLMAX(self, sew, lmul, VLEN=1024):
        return int(factor_lmul[str(lmul)]*VLEN/sew)


    def intdtype(self):
        int_dtype_dict  = { 8: np.int8,  16: np.int16,  32: np.int32,  64: np.int64 }
        return int_dtype_dict[self['sew']]

    def uintdtype(self):
        uint_dtype_dict = { 8: np.uint8, 16: np.uint16, 32: np.uint32, 64: np.uint64 }
        return uint_dtype_dict[self['sew']]       
