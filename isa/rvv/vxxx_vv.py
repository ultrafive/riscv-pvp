from isa.inst import *
import numpy as np
import math

class Vadd_vv(Inst):
    name = 'vadd.vv'

    def golden(self):
        return self.masked(self['vs2'] + self['vs1'])

class Vsub_vv(Inst):
    name = 'vsub.vv'

    def golden(self):
        return self.masked(self['vs2'] - self['vs1'])

class Vmin_vv(Inst):
    name = 'vmin.vv'

    def golden(self):
        return self.masked(np.minimum(self['vs2'], self['vs1']))

class Vminu_vv(Inst):
    name = 'vminu.vv'

    def golden(self):
        return self.masked(np.minimum(self['vs2'], self['vs1']))

class Vmax_vv(Inst):
    name = 'vmax.vv'

    def golden(self):
        return self.masked(np.maximum(self['vs2'], self['vs1']))

class Vmaxu_vv(Inst):
    name = 'vmaxu.vv'

    def golden(self):
        return self.masked(np.maximum(self['vs2'], self['vs1']))

class Vand_vv(Inst):
    name = 'vand.vv'

    def golden(self):
        return self.masked(self['vs2'] & self['vs1'])

class Vor_vv(Inst):
    name = 'vor.vv'

    def golden(self):
        return self.masked(self['vs2'] | self['vs1'])

class Vxor_vv(Inst):
    name = 'vxor.vv'

    def golden(self):
        return self.masked(self['vs2'] ^ self['vs1'])