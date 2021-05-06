from isa.inst import *
import numpy as np
import math

class Vadd_vx(Inst):
    name = 'vadd.vx'

    def golden(self):
        return self.masked(self['vs2'] + self['rs1'])

class Vsub_vx(Inst):
    name = 'vsub.vx'

    def golden(self):
        return self.masked(self['vs2'] - self['rs1'])

class Vrsub_vx(Inst):
    name = 'vrsub.vx'

    def golden(self):
        return self.masked(self['rs1'] - self['vs2'])

class Vmin_vx(Inst):
    name = 'vmin.vx'

    def golden(self):
        return self.masked(np.minimum(self['vs2'], self['rs1']))

class Vminu_vx(Inst):
    name = 'vminu.vx'

    def golden(self):
        return self.masked(np.minimum(self['vs2'], self['rs1']))

class Vmax_vx(Inst):
    name = 'vmax.vx'

    def golden(self):
        return self.masked(np.maximum(self['vs2'], self['rs1']))

class Vmaxu_vx(Inst):
    name = 'vmaxu.vx'

    def golden(self):
        return self.masked(np.maximum(self['vs2'], self['rs1']))

class Vand_vx(Inst):
    name = 'vand.vx'

    def golden(self):
        return self.masked(self['vs2'] & self['rs1'])

class Vor_vx(Inst):
    name = 'vor.vx'

    def golden(self):
        return self.masked(self['vs2'] | self['rs1'])

class Vxor_vx(Inst):
    name = 'vxor.vx'

    def golden(self):
        return self.masked(self['vs2'] ^ self['rs1'])