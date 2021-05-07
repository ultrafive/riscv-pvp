from isa.inst import *
import numpy as np
import math

class Vadd_vi(Inst):
    name = 'vadd.vi'

    def golden(self):
        return self.masked(self['vs2'] + self['imm'])

class Vrsub_vi(Inst):
    name = 'vrsub.vi'

    def golden(self):
        return self.masked(self['imm'] - self['vs2'])

class Vand_vi(Inst):
    name = 'vand.vi'

    def golden(self):
        return self.masked(self['vs2'] & self['imm'])

class Vor_vi(Inst):
    name = 'vor.vi'

    def golden(self):
        return self.masked(self['vs2'] | self['imm'])

class Vxor_vi(Inst):
    name = 'vxor.vi'

    def golden(self):
        return self.masked(self['vs2'] ^ self['imm'])

class Vsll_vi(Inst):
    name = 'vsll.vi'

    def golden(self):
        return self.masked(self['vs2'] << self['imm'])

class Vsrl_vi(Inst):
    name = 'vsrl.vi'

    def golden(self):
        return self.masked(self['vs2'] >> self['imm'])

class Vsra_vi(Inst):
    name = 'vsra.vi'

    def golden(self):
        return self.masked(self['vs2'] >> self['imm'])