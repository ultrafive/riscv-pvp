
import sys
import numpy as np

class Inst(dict):
    name = 'unknown'

    def golden(self):
        raise NotImplementedError()

    def masked(self, value, old = 0, vstart = 0):
        if 'mask' not in self:
            return value
        else:
            mask = np.unpackbits(self['mask'], bitorder='little')[vstart: self['vlen']]
            return np.where( mask == 1, value, old)


    def as_mask(self, value):
        return np.packbits(np.unpackbits(value, bitorder='little')[0: self['vlen']], bitorder='little')


    def where(self):
        if 'mask' not in self:
            return True
        else:
            return np.unpackbits(self['mask'], bitorder='little')[0: self['vlen']] == 1
    
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


    def rounding(self, result, xrm, shift):
        # Suppose the pre-rounding result is v, and d bits of that result areto be rounded off. 
        # Then the rounded result is (v >> d) + r, where r depends on the rounding mode 
        # (result >> shift) + r
        lsb = 1 << (shift)
        lsb_half = lsb >> 1

        if xrm == 0:    #RNU:
            result += lsb_half
        elif xrm == 1:  #RNE:
            if (result & lsb_half) and ((result & (lsb_half-1)) or (result & lsb)) :
                result += lsb
        elif xrm == 2:  #RDN:
            pass
        elif xrm == 3:  #ROD:
            if result & (lsb - 1):
                result |= lsb
        else:
            print("error vrm para!")

        return result