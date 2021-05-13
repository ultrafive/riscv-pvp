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

class Vsll_vv(Inst):
    name = 'vsll.vv'

    def golden(self):
        return self.masked(self['vs2'] << self['vs1'])


class Vsrl_vv(Inst):
    name = 'vsrl.vv'

    def golden(self):
        return self.masked(self['vs2'] >> self['vs1'])

class Vsra_vv(Inst):
    name = 'vsra.vv'

    def golden(self):
        return self.masked(self['vs2'] >> self['vs1'])

class Vmul_vv(Inst):
    name = 'vmul.vv'

    def golden(self):
        return self.masked(self['vs2'] * self['vs1'])

class Vmulh_vv(Inst):
    name = 'vmulh.vv'

    def golden(self):
        vd = self['vs2'].astype(np.int64) * self['vs1'].astype(np.int64)
        vd = vd >> np.array([32], dtype=np.uint8)
        vd = vd. astype(np.int32)

        return self.masked(vd)

class Vmulhu_vv(Inst):
    name = 'vmulhu.vv'

    def golden(self):

        vd = self['vs2'].astype(np.uint64) * self['vs1'].astype(np.uint64)
        vd = vd >> np.array([32], dtype=np.uint8)
        vd = vd. astype(np.uint32)

        return self.masked(vd)

class Vmulhsu_vv(Inst):
    name = 'vmulhsu.vv'

    def golden(self):

        vd = self['vs2'].astype(np.int64) * self['vs1']
        vd = vd.astype(np.int64) >> np.array([32], dtype=np.uint8)
        vd = vd. astype(np.int32)

        return self.masked(vd)

class Vdivu_vv(Inst):
    name = 'vdivu.vv'

    def golden(self):
        vd = (self['vs2'] / self['vs1']).astype(self['vs2'].dtype)

        return self.masked(vd)

class Vdiv_vv(Inst):
    name = 'vdiv.vv'

    def golden(self):
        vd = (self['vs2'] / self['vs1']).astype(self['vs2'].dtype)

        return self.masked(vd)

class Vremu_vv(Inst):
    name = 'vremu.vv'

    def golden(self):
        return self.masked(self['vs2'] % self['vs1'])

class Vrem_vv(Inst):
    name = 'vrem.vv'

    def golden(self):
        vd = self['vs2'] - self['vs1'] * (self['vs2'] // self['vs1'])
        return self.masked(vd)
