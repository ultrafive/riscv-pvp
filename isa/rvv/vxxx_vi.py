from isa.inst import *
import numpy as np
import math

class Vadd_vi(Inst):
    name = 'vadd.vi'

    def golden(self):
        return self.masked(self['vs2'] + np.array(self['imm']))

class Vrsub_vi(Inst):
    name = 'vrsub.vi'

    def golden(self):
        return self.masked(np.array(self['imm']) - self['vs2'])

class Vand_vi(Inst):
    name = 'vand.vi'

    def golden(self):
        return self.masked(self['vs2'] & np.array(self['imm']))

class Vor_vi(Inst):
    name = 'vor.vi'

    def golden(self):
        return self.masked(self['vs2'] | np.array(self['imm']))

class Vxor_vi(Inst):
    name = 'vxor.vi'

    def golden(self):
        return self.masked(self['vs2'] ^ np.array(self['imm']))