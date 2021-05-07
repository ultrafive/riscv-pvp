from isa.inst import *
import numpy as np

class Vwaddu_vv(Inst):
    name = 'vwaddu.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) + self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) + self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) + self['vs1']
        
        return self.masked(vd)

class Vwadd_vv(Inst):
    name = 'vwadd.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) + self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) + self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) + self['vs1']

        return self.masked(vd)

class Vwsubu_vv(Inst):
    name = 'vwsubu.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) - self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) - self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) - self['vs1']
        
        return self.masked(vd)

class Vwsub_vv(Inst):
    name = 'vwsub.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) - self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) - self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) - self['vs1']
        
        return self.masked(vd)

class Vwmul_vv(Inst):
    name = 'vwmul.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) * self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) * self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) * self['vs1']
        
        return self.masked(vd)

class Vwmulu_vv(Inst):
    name = 'vwmulu.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.uint64) * self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.uint32) * self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.uint16) * self['vs1']
        
        return self.masked(vd)

class Vwmulsu_vv(Inst):
    name = 'vwmulsu.vv'

    def golden(self):
        if self['ebits'] == 32:
            vd = self['vs2'].astype(np.int64) * self['vs1']
        elif self['ebits'] == 16:
            vd = self['vs2'].astype(np.int32) * self['vs1']
        elif  self['ebits'] == 8:
            vd = self['vs2'].astype(np.int16) * self['vs1']
        
        return self.masked(vd)
