from isa.inst import *
import numpy as np

class Vwmaccu_vx(Inst):
    name = 'vwmaccu.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) * self['rs1'] + self['vd']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) * self['rs1'] + self['vd']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) * self['rs1'] + self['vd']

        return self.masked(vd, old = self['vd'])

class Vwmacc_vx(Inst):
    name = 'vwmacc.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) * self['rs1'] + self['vd']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) * self['rs1'] + self['vd']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) * self['rs1'] + self['vd']

        return self.masked(vd, old = self['vd'])

class Vwmaccsu_vx(Inst):
    name = 'vwmaccsu.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) * self['rs1'] + self['vd']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) * self['rs1'] + self['vd']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) * self['rs1'] + self['vd']
        
        return self.masked(vd, old = self['vd'])

class Vwmaccus_vx(Inst):
    name = 'vwmaccus.vx'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) * self['rs1'] + self['vd']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) * self['rs1'] + self['vd']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) * self['rs1'] + self['vd']
        
        return self.masked(vd, old = self['vd'])