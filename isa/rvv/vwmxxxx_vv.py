from isa.inst import *
import numpy as np

class Vwmaccu_vv(Inst):
    name = 'vwmaccu.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs1'].astype(np.uint64) * self['vs2'] + self['vd']
        elif self['ebits'] == 16:
            vd = self['vs1'].astype(np.uint32) * self['vs2'] + self['vd']
        elif  self['ebits'] == 8:
            vd = self['vs1'].astype(np.uint16) * self['vs2'] + self['vd']
        
        return self.masked(vd, old = self['vd'])

class Vwmacc_vv(Inst):
    name = 'vwmacc.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs1'].astype(np.int64) * self['vs2'] + self['vd']
        elif self['ebits'] == 16:
            vd = self['vs1'].astype(np.int32) * self['vs2'] + self['vd']
        elif  self['ebits'] == 8:
            vd = self['vs1'].astype(np.int16) * self['vs2'] + self['vd']
        
        return self.masked(vd, old = self['vd'])

class Vwmaccsu_vv(Inst):
    name = 'vwmaccsu.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs1'].astype(np.int64) * self['vs2'] + self['vd']
        elif self['ebits'] == 16:
            vd = self['vs1'].astype(np.int32) * self['vs2'] + self['vd']
        elif  self['ebits'] == 8:
            vd = self['vs1'].astype(np.int16) * self['vs2'] + self['vd']
        
        return self.masked(vd, old = self['vd'])