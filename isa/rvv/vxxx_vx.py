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

class Vsll_vx(Inst):
    name = 'vsll.vx'

    def golden(self):
         return self.masked(self['vs2'] << self['rs1'])

class Vsrl_vx(Inst):
    name = 'vsrl.vx'

    def golden(self):
         return self.masked(self['vs2'] >> self['rs1'])

class Vsra_vx(Inst):
    name = 'vsra.vx'

    def golden(self):
         return self.masked(self['vs2'] >> self['rs1'])

class Vmul_vx(Inst):
    name = 'vmul.vx'

    def golden(self):
        return self.masked(self['vs2'] * self['rs1'])

class Vmulh_vx(Inst):
    name = 'vmulh.vx'

    def golden(self):
        vd = self['vs2'].astype(np.int64) * self['rs1']
        vd = vd >> np.array([32], dtype=np.uint8)
        vd = vd. astype(np.int32)

        return self.masked(vd)

class Vmulhu_vx(Inst):
    name = 'vmulhu.vx'

    def golden(self):

        vd = self['vs2'].astype(np.uint64) * self['rs1']
        vd = vd >> np.array([32], dtype=np.uint8)
        vd = vd. astype(np.uint32)

        return self.masked(vd)

class Vmulhsu_vx(Inst):
    name = 'vmulhsu.vx'

    def golden(self):
        if self['vs2'].dtype == 'int32' or self['vs2'].dtype == 'uint32':
            vd = self['vs2'].astype(np.int64) * self['rs1']
            vd = vd.astype(np.int64) >> np.array([32], dtype=np.uint8)
            vd = vd. astype(np.int32)
        elif self['vs2'].dtype == 'int16' or self['vs2'].dtype == 'int16':
            vd = self['vs2'].astype(np.int32) * self['rs1']
            vd = vd.astype(np.int32) >> np.array([16], dtype=np.uint8)
            vd = vd. astype(np.int16)
        else:
            vd = self['vs2'].astype(np.int16) * self['rs1']
            vd = vd.astype(np.int16) >> np.array([8], dtype=np.uint8)
            vd = vd. astype(np.int8)
        
        return self.masked(vd)

class Vdivu_vx(Inst):
    name = 'vdivu.vx'

    def golden(self):
        return self.masked((self['vs2'] / self['rs1']).astype(self['vs2'].dtype))

class Vdiv_vx(Inst):
    name = 'vdiv.vx'

    def golden(self):
        return self.masked((self['vs2'] / self['rs1']).astype(self['vs2'].dtype))

class Vremu_vx(Inst):
    name = 'vremu.vx'

    def golden(self):
        return self.masked(self['vs2'] % self['rs1'])

class Vrem_vx(Inst):
    name = 'vrem.vx'

    def golden(self):
        vd = np.fmod(self['vs2'], self['rs1'])
        return self.masked(vd)