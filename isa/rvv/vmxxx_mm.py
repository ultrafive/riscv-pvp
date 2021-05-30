from isa.inst import *
import numpy as np
import math

class Vmand_mm(Inst):
    name = 'vmand.mm'

    def golden(self):
        return self.as_mask(self['vs2'] & self['vs1'])

class Vmnand_mm(Inst):
    name = 'vmnand.mm'

    def golden(self):
        return self.as_mask(~(self['vs2'] & self['vs1']))

class Vmandnot_mm(Inst):
    name = 'vmandnot.mm'

    def golden(self):
        return self.as_mask(self['vs2'] & ~(self['vs1']))

class Vmxor_mm(Inst):
    name = 'vmxor.mm'

    def golden(self):
        return self.as_mask(self['vs2'] ^ self['vs1'])

class Vmor_mm(Inst):
    name = 'vmor.mm'

    def golden(self):
        return self.as_mask(self['vs2'] | self['vs1'])

class Vmnor_mm(Inst):
    name = 'vmnor.mm'

    def golden(self):
        return self.as_mask(~(self['vs2'] | self['vs1']))

class Vmornot_mm(Inst):
    name = 'vmornot.mm'

    def golden(self):
        return self.as_mask(self['vs2'] | ~(self['vs1']))

class Vmxnor_mm(Inst):
    name = 'vmxnor.mm'

    def golden(self):
        return self.as_mask(~(self['vs2'] ^ self['vs1']))