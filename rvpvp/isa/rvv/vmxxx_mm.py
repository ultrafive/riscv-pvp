from ...isa.inst import *
import numpy as np
import math

class Vmxxx_mm(Inst):
    name = 'vmxxx_mm'

    def golden(self):
        if 'orign' in self:
            result = self['orign'].copy()
        elif 'dst' in self:
            if self['dst'] == 0:
                result = self['vs1'].copy()
            elif self['dst'] == 1:
                result = self['vs2'].copy()
            elif self['dst'] == 2:
                result = self['vs1'].copy()
        else:
            result = np.zeros(self['vl'], dtype=np.uint8)
            result = np.packbits(np.unpackbits(result, bitorder='little')[0: self['vl']], bitorder='little')

        if 'start' in self:
            start = self['start']
            if self['start'] >= self['vl']:
                return result
        else: 
            start = 0
        
        vs1 = self['vs1']
        if 'vs2' in self:
            vs2 = self['vs2']
        else:
            vs2 = self['vs1']

        if 'vmand.mm' in self.name:
            res = vs2 & vs1
        elif 'vmnand.mm' in self.name:
            res = ~(vs2 & vs1)
        elif 'vmandnot.mm' in self.name:
            res = vs2 & (~vs1)
        elif 'vmxor.mm' in self.name:
            res = vs2 ^ vs1
        elif 'vmor.mm' in self.name:
            res = vs2 | vs1
        elif 'vmnor.mm' in self.name:
            res = ~(vs2 | vs1)
        elif 'vmornot.mm' in self.name:
            res = vs2 | (~vs1)
        elif 'vmxnor.mm' in self.name:
            res = ~(vs2 ^ vs1)

        result =  self.bits_copy(np.packbits(np.unpackbits(res, bitorder='little')[0: self['vl']], bitorder='little'), result, start)
        return result


class Vmand_mm(Vmxxx_mm):
    name = 'vmand.mm'

class Vmnand_mm(Vmxxx_mm):
    name = 'vmnand.mm'

class Vmandnot_mm(Vmxxx_mm):
    name = 'vmandnot.mm'

class Vmxor_mm(Vmxxx_mm):
    name = 'vmxor.mm'

class Vmor_mm(Vmxxx_mm):
    name = 'vmor.mm'

class Vmnor_mm(Vmxxx_mm):
    name = 'vmnor.mm'

class Vmornot_mm(Vmxxx_mm):
    name = 'vmornot.mm'
   
class Vmxnor_mm(Vmxxx_mm):
    name = 'vmxnor.mm'
