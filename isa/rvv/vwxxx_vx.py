from isa.inst import *
import numpy as np

class Vwaddu_vx(Inst):
    name = 'vwaddu.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) + self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) + self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) + self['rs1']
        
        return self.masked(vd)

class Vwadd_vx(Inst):
    name = 'vwadd.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) + self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) + self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) + self['rs1']
        
        return self.masked(vd)

class Vwsubu_vx(Inst):
    name = 'vwsubu.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) - self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) - self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) - self['rs1']
        
        return self.masked(vd)

class Vwsub_vx(Inst):
    name = 'vwsub.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) - self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) - self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) - self['rs1']
        
        return self.masked(vd)


class Vmul_vx(Inst):
    name = 'vmul.vx'

    def golden(self):
        return self.masked(self['vs2'] * self['rs1'])

class Vwmulu_vx(Inst):
    name = 'vwmulu.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) * self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) * self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) * self['rs1']
        
        return self.masked(vd)

class Vwmulsu_vx(Inst):
    name = 'vwmulsu.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) * self['rs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) * self['rs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) * self['rs1']

        return self.masked(vd)